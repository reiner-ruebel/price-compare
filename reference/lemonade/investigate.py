"""Bounded reproduction of the supplied questionnaire. Private runs contain session data."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE = "https://chat-api.lemonade.com/chat/public/scripts/gb-home-quote"
ROOT = Path(__file__).resolve().parent


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def step_summary(data):
    step = data["history"][-1]
    return {"name": step.get("name"), "status": step.get("status"),
            "keys": list(step), "rendered": step.get("renderedStep"),
            "payload": step.get("payload")}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", type=Path, help="Resume a private run directory")
    ap.add_argument("--case", type=Path, default=ROOT / "case-owner-example.json")
    ap.add_argument("--advance", type=int, default=0, help="Maximum answers to submit in this invocation")
    ap.add_argument("--expected-step", help="Exact current step name, required before submitting one answer")
    args = ap.parse_args()
    case = json.loads(args.case.read_text(encoding="utf-8"))
    run = args.run or ROOT / "runs" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"accept": "application/json", "content-type": "application/json",
                            "origin": "https://chat.lemonade.com", "referer": "https://chat.lemonade.com/"})
    state_path = run / "state.private.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        for cookie in state["cookies"]:
            session.cookies.set_cookie(requests.cookies.create_cookie(**cookie))
        data = state["data"]
        index = state["answer_index"]
        case = state["case"]
    else:
        data = None
        index = 0
        if not case.get("email"):
            case["email"] = "lemonade_test_" + str(int(datetime.now(timezone.utc).timestamp())) + "@example.com"

    def checkpoint():
        cookies = [{key: getattr(c, key) for key in ("name", "value", "domain", "path", "secure", "expires")} for c in session.cookies]
        save(state_path, {"answer_index": index, "case": case, "cookies": cookies, "data": data})
        save(run / f"{index:02d}-step.private.json", step_summary(data))

    def post(url, body):
        response = session.post(url, json=body, timeout=(10, 60))
        print("HTTP", response.status_code, response.headers.get("content-type", ""))
        if not response.ok:
            (run / "http-error.private.txt").write_text(response.text, encoding="utf-8")
            response.raise_for_status()
        return response.json()

    if data is None:
        data = post(BASE + "/sessions", {"forceRestart": False})
        checkpoint()
    print("Run:", run)
    print("Current step:", data["history"][-1].get("name"), "answer index:", index)
    if args.advance not in (0, 1):
        raise ValueError("Diagnostic runner currently permits only one checked answer per invocation")
    if args.advance:
        step = data["history"][-1]
        if step.get("name") != args.expected_step:
            raise ValueError("Expected step mismatch; no answer submitted")
        prop = case["property"]
        answers = [
            {"insured": case["insured"]},
            {"addressToInsure": {"postalCode": case["postal_code"]}},
            None,
            *[{"property": {key: prop[key]}} for key in ("relationToProperty", "dwellingType", "coverageType", "declaredPrimaryResidence", "daytimeOccupation", "roofMaterial", "declaredGoodHouseCondition")],
            *[{key: case[key]} for key in ("protectiveDevicesArray", "additionalResidentsArray", "expensiveItems", "userReportedClaims", "pastInsuranceCancellations", "criminalHistory")],
            {"accountDetails": {"email": case["email"], "dateOfBirth": case["date_of_birth"], "compliance": case["compliance"]}},
            {}
        ]
        if index >= len(answers):
            raise ValueError("Supplied sequence complete; no further writes permitted")
        answer = answers[index]
        if index == 2:
            content = step["renderedStep"]["presentation"]["component"]["content"]
            items = content[0]["elements"][0]["items"]
            matches = [x for x in items if case["address_label_contains"].lower() in x.get("label", "").lower()]
            if len(matches) != 1:
                raise ValueError(f"Expected exactly one matching address, got {len(matches)}")
            answer = {"addressProviderId": matches[0]["value"]}
        data = post(f"{BASE}/sessions/{data['sessionId']}/steps/{step['id']}", {"answers": answer, "skipHooks": False})
        index += 1
        checkpoint()
        print("Next step:", data["history"][-1].get("name"), "answer index:", index)
    summary = step_summary(data)
    print("Step fields:", list(summary.get("rendered") or {}))


if __name__ == "__main__":
    main()
