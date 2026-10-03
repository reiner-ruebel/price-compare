"""Single-case Lemonade UK quote proof of concept. Never advances to checkout."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import requests

API = "https://chat-api.lemonade.com/chat/public/scripts/"
ROOT = Path(__file__).resolve().parent
SEQUENCE = (
    "user-name", "address-to-insure", "confirm-address", "tenant-or-property-owner",
    "dwelling", "coverage-type", "primary-residence", "daytime-occupation", "roof-material",
    "house-condition", "security-measures", "other-residents", "expensive-items",
    "past-home-claims", "past-insurance-cancellation-by-insurer", "criminal-history",
    "account-details-for-new-user", "calculating-price",
)


class StopRun(Exception):
    def __init__(self, status, detail):
        self.status, self.detail = status, detail
        super().__init__(detail)


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def quote_request(redirect):
    if not isinstance(redirect, str):
        raise StopRun("unexpected_response", "Quote redirect is missing")
    parsed = urlsplit(redirect.strip('"'))
    if parsed.scheme != "https" or parsed.hostname != "chat.lemonade.com" or parsed.port not in (None, 443) or parsed.username or parsed.password or parsed.path != "/gb/home/quote/view":
        raise StopRun("unexpected_response", "Quote redirect does not match the observed UK quote route")
    query = parse_qs(parsed.query, keep_blank_values=True)
    if any(len(v) != 1 for v in query.values()):
        raise StopRun("unexpected_response", "Ambiguous quote parameters")
    reference = query.get("quotePublicId", [""])[0]
    product = query.get("product", [""])[0]
    bridging = query.get("bridging", [""])[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{5,100}", reference) or product != "homeowners-gb" or bridging not in ("true", "false"):
        raise StopRun("unexpected_response", "Quote parameters differ from the observed homeowners journey")
    return {"data": {"quotePublicId": reference, "product": product, "bridging": bridging == "true"}, "forceRestart": False}


def extract_quote(data):
    """Use the exact quote summary, never the first currency amount or an add-on price."""
    try:
        step = data["history"][-1]
        if step["name"] != "quote":
            raise StopRun("unexpected_step", "Quote-view service did not return the observed quote step")
        rendered = step["renderedStep"]
        summary = rendered["presentation"]["frame"]["summary"]
        if summary.get("type") != "price":
            raise StopRun("unverified_result", "No recognised quote price summary")
        match = re.fullmatch(r"£([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+)\.([0-9]{2})", summary["price"].strip())
        if not match or summary.get("period") not in ("mo", "yr"):
            raise StopRun("unverified_result", "Unrecognised currency, amount or billing period")
        amount = Decimal(match[1].replace(",", "") + "." + match[2])
        if amount <= 0:
            raise StopRun("unverified_result", "Non-positive price requires review")
        values = rendered["data"]["values"]
        return {
            "supplier_brand": "Lemonade",
            "product_label": "Buildings and contents (owner-selected cover)",
            "premium_amount": str(amount), "currency": "GBP",
            "premium_period": {"mo": "month", "yr": "year"}[summary["period"]],
            "displayed_price": summary["price"],
            "premium_source": "history[-1].renderedStep.presentation.frame.summary",
            "benefits_displayed": summary.get("benefits", []),
            "quote_configuration": values,
            "annual_premium": str(amount) if summary["period"] == "yr" else None,
            "notes": ["Displayed quote only; no checkout or purchase performed.",
                      "Supplier brand and selected cover are not verification of the legal underwriting entity.",
                      "Default cover limits, excesses and start date were returned by the supplier; they were not selected by this runner.",
                      "A monthly amount is not an independently obtained annual premium."],
        }
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        raise StopRun("unexpected_response", "Quote response no longer has the observed structure") from exc


def validate_case(case):
    try:
        for field in ("case_id", "postal_code", "address_label_contains", "date_of_birth"):
            if not isinstance(case[field], str) or not case[field].strip():
                raise ValueError(field)
        for field in ("firstName", "lastName"):
            if not isinstance(case["insured"][field], str) or not case["insured"][field].strip():
                raise ValueError(field)
        prop = case["property"]
        if prop["relationToProperty"] != "owner" or prop["coverageType"] != "buildings_and_contents":
            raise ValueError("Only the observed owner/buildings-and-contents route is supported")
        for field in ("dwellingType", "roofMaterial"):
            if not isinstance(prop[field], str) or not prop[field]:
                raise ValueError(field)
        for field in ("declaredPrimaryResidence", "daytimeOccupation", "declaredGoodHouseCondition"):
            if not isinstance(prop[field], bool):
                raise ValueError(field)
        for field in ("protectiveDevicesArray", "additionalResidentsArray"):
            if not isinstance(case[field], list):
                raise ValueError(field)
        for field in ("expensiveItems", "pastInsuranceCancellations", "criminalHistory"):
            if not isinstance(case[field], bool):
                raise ValueError(field)
        if not isinstance(case["userReportedClaims"], str):
            raise ValueError("userReportedClaims")
        datetime.strptime(case["date_of_birth"], "%Y-%m-%d")
        if case["compliance"] != {"marketingTermsApproved": False, "termsOfServiceApproved": True}:
            raise ValueError("Compliance values differ from the supplied test flow")
        if case.get("email") is not None and (not isinstance(case["email"], str) or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", case["email"])):
            raise ValueError("email")
    except (KeyError, TypeError, ValueError) as exc:
        raise StopRun("invalid_input", f"Missing or unsupported case field: {exc}") from exc


def answer_for(case, index, step):
    if step.get("name") != SEQUENCE[index] or step.get("status") != "pending":
        raise StopRun("unexpected_step", f"Expected {SEQUENCE[index]}; stopped without answering a different question")
    prop = case["property"]
    answers = [
        {"insured": case["insured"]}, {"addressToInsure": {"postalCode": case["postal_code"]}}, None,
        *[{"property": {key: prop[key]}} for key in ("relationToProperty", "dwellingType", "coverageType", "declaredPrimaryResidence", "daytimeOccupation", "roofMaterial", "declaredGoodHouseCondition")],
        *[{key: case[key]} for key in ("protectiveDevicesArray", "additionalResidentsArray", "expensiveItems", "userReportedClaims", "pastInsuranceCancellations", "criminalHistory")],
        {"accountDetails": {"email": case["email"], "dateOfBirth": case["date_of_birth"], "compliance": case["compliance"]}}, {},
    ]
    if index == 2:
        try:
            items = step["renderedStep"]["presentation"]["component"]["content"][0]["elements"][0]["items"]
            matches = [x for x in items if case["address_label_contains"].casefold() in x["label"].casefold()]
            if len(matches) != 1:
                raise StopRun("invalid_input", f"Address selection has {len(matches)} matches; requires exactly one")
            return {"addressProviderId": matches[0]["value"]}
        except (KeyError, IndexError, TypeError) as exc:
            raise StopRun("unexpected_response", "Address lookup format changed") from exc
    return answers[index]


def collect(case, output, save_private=False):
    started = time.monotonic()
    session = requests.Session()
    session.headers.update({"accept": "application/json", "content-type": "application/json",
                            "origin": "https://chat.lemonade.com", "referer": "https://chat.lemonade.com/"})
    count = 0

    def post(script, suffix, body):
        nonlocal count
        if time.monotonic() - started > 600 or count >= 20:
            raise StopRun("technical_failure", "Run safety bound reached")
        count += 1
        try:
            response = session.post(API + script + suffix, json=body, timeout=(10, 60), allow_redirects=False)
        except requests.Timeout as exc:
            raise StopRun("pending_timeout", "Request timed out; no automatic resubmission") from exc
        except requests.RequestException as exc:
            raise StopRun("technical_failure", "Network request failed; no automatic resubmission") from exc
        if save_private:
            (output / f"{count:02d}-response.private.txt").write_bytes(response.content)
        if response.status_code != 201:
            status = {401: "authentication_required", 403: "access_denied", 429: "rate_limited"}.get(response.status_code, "technical_failure")
            raise StopRun(status, f"Service returned HTTP {response.status_code}; stopped without retry")
        try:
            return response.json()
        except ValueError as exc:
            raise StopRun("unexpected_response", "Service returned a non-JSON response") from exc

    try:
        data = post("gb-home-quote", "/sessions", {"forceRestart": False})
        for index, expected in enumerate(SEQUENCE):
            step = data["history"][-1]
            answer = answer_for(case, index, step)
            print(f"{index + 1:02d}/{len(SEQUENCE)} {expected}", flush=True)
            # Session/step IDs come from this run, never from another user's session.
            session_id, step_id = data["sessionId"], step["id"]
            if not all(isinstance(v, str) and re.fullmatch(r"[A-Za-z0-9_-]+", v) for v in (session_id, step_id)):
                raise StopRun("unexpected_response", "Invalid session or step identifier")
            data = post("gb-home-quote", f"/sessions/{session_id}/steps/{step_id}", {"answers": answer, "skipHooks": False})
        final = data["history"][-1]
        if final["name"] != "home-gb-onboarding-done":
            raise StopRun("unexpected_step", "Questionnaire did not end at the observed quote redirect")
        body = quote_request(final["payload"]["redirectTo"])
        if save_private:
            cookies = [{k: getattr(c, k) for k in ("name", "value", "domain", "path", "secure", "expires")} for c in session.cookies]
            save_json(output / "state.private.json", {"data": data, "cookies": cookies, "case": case, "answer_index": 18})
        quote_data = post("gb-home-quote-view", "/sessions", body)
        result = extract_quote(quote_data)
        result.update({"status": "quoted", "quote_reference": body["data"]["quotePublicId"], "request_count": count,
                       "elapsed_seconds": round(time.monotonic() - started, 2)})
        return result
    except (KeyError, IndexError, TypeError) as exc:
        raise StopRun("unexpected_response", "Questionnaire response structure changed") from exc
    finally:
        session.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--case", type=Path, default=ROOT / "case-owner-example.json")
    ap.add_argument("--output", type=Path, help="New empty results directory; existing results are not overwritten")
    ap.add_argument("--confirm-test-submission", action="store_true", help="Confirm this supplied/approved test may be submitted, including its account/terms answers")
    ap.add_argument("--save-private", action="store_true", help="Save full responses and session cookies for local diagnosis; do not share these files")
    args = ap.parse_args()
    if not args.confirm_test_submission:
        ap.error("No live request made. Review the test case, then use --confirm-test-submission to submit it.")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output = args.output or ROOT / "runs" / run_id
    output.mkdir(parents=True, exist_ok=False)
    result = {"run_id": run_id, "observed_at_utc": datetime.now(timezone.utc).isoformat(), "status": "technical_failure"}
    try:
        raw = args.case.read_bytes()
        case = json.loads(raw.decode("utf-8-sig"))
        validate_case(case)
        result.update({"case_id": case["case_id"], "input_sha256": hashlib.sha256(raw).hexdigest()})
        if not case.get("email"):
            case["email"] = f"lemonade_test_{int(time.time())}_{uuid.uuid4().hex[:6]}@example.com"
        result.update(collect(case, output, args.save_private))
    except StopRun as exc:
        result.update({"status": exc.status, "detail": exc.detail})
    except (OSError, ValueError) as exc:
        result.update({"status": "invalid_input", "detail": f"Could not process input/output: {type(exc).__name__}"})
    save_json(output / "result.json", result)
    fields = ("run_id", "case_id", "status", "supplier_brand", "product_label", "premium_amount", "currency", "premium_period", "quote_reference", "observed_at_utc", "detail")
    with (output / "result.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerow(result)
    print("Result:", result["status"], result.get("premium_amount", ""), result.get("currency", ""), result.get("premium_period", ""))
    print("Saved:", output.resolve())
    return 0 if result["status"] == "quoted" else 2


if __name__ == "__main__":
    sys.exit(main())
