"""Offline tests: no insurer requests, no real case data, no browser required."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from collect_quote import SEQUENCE, StopRun, answer_for, collect, extract_quote, quote_request, validate_case


def quote_fixture():
    return {"history": [{"name": "quote", "renderedStep": {
        "presentation": {"frame": {"summary": {"type": "price", "price": "£51.92", "period": "mo", "benefits": ["Contents £10K"]}}},
        "data": {"values": {"quote.limits.contents": 10000}},
    }}]}


def case_fixture():
    # Used offline only. The separate supplied case is loaded only for validation tests.
    value = json.loads((Path(__file__).parent / "case-owner-example.json").read_text(encoding="utf-8"))
    value["email"] = "offline-test@example.com"
    return value


def address_step(labels):
    return {"name": "confirm-address", "status": "pending", "renderedStep": {
        "presentation": {"component": {"content": [{"elements": [{"items": [{"label": label, "value": str(i)} for i, label in enumerate(labels)]}]}]}}}}


class Response:
    def __init__(self, data, status=201):
        self.data, self.status_code = data, status
        self.content = json.dumps(data).encode()

    def json(self):
        return self.data


class FakeSession:
    def __init__(self, failure=None):
        self.headers = {}
        self.cookies = []
        self.calls = []
        self.failure = failure

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if isinstance(self.failure, Exception):
            raise self.failure
        if self.failure:
            return Response({}, self.failure)
        index = len(self.calls) - 1
        if index == 19:
            return Response(quote_fixture())
        if index == 18:
            step = {"name": "home-gb-onboarding-done", "payload": {"redirectTo": "https://chat.lemonade.com/gb/home/quote/view?quotePublicId=TEST1234&product=homeowners-gb&bridging=false"}}
        else:
            step = {"name": SEQUENCE[index], "status": "pending"}
            if index == 2:
                step = address_step(["Little Haven, Test Road"])
            step["id"] = f"step-{index}"
        return Response({"sessionId": "offline-session", "history": [step]})

    def close(self):
        pass


class QuoteTests(unittest.TestCase):
    def test_monthly_exact_summary(self):
        result = extract_quote(quote_fixture())
        self.assertEqual((result["premium_amount"], result["currency"], result["premium_period"]), ("51.92", "GBP", "month"))
        self.assertIsNone(result["annual_premium"])

    def test_annual_period(self):
        data = quote_fixture()
        data["history"][0]["renderedStep"]["presentation"]["frame"]["summary"].update(price="£1,234.56", period="yr")
        result = extract_quote(data)
        self.assertEqual((result["premium_amount"], result["premium_period"]), ("1234.56", "year"))

    def test_never_pick_add_on(self):
        data = quote_fixture()
        data["advertisement"] = {"price": "£3.00"}
        self.assertEqual(extract_quote(data)["premium_amount"], "51.92")

    def test_reject_unrecognised_prices(self):
        for price in ("$51.92", "£0.00", "£-1.00", "from £51.92", "£51", "£1,23.45", "Â£51.92"):
            with self.subTest(price=price), self.assertRaises(StopRun):
                data = quote_fixture()
                data["history"][0]["renderedStep"]["presentation"]["frame"]["summary"]["price"] = price
                extract_quote(data)

    def test_reject_unknown_period(self):
        data = quote_fixture()
        data["history"][0]["renderedStep"]["presentation"]["frame"]["summary"]["period"] = "week"
        with self.assertRaises(StopRun):
            extract_quote(data)

    def test_missing_premium_does_not_succeed(self):
        for data in ({}, {"history": []}, {"history": [{"name": "declined"}]}, {"history": [{"name": "quote"}]}):
            with self.subTest(data=data), self.assertRaises(StopRun):
                extract_quote(data)

    def test_redirect_boolean_and_id(self):
        value = quote_request('"https://chat.lemonade.com/gb/home/quote/view?quotePublicId=TEST1234&product=homeowners-gb&bridging=false"')
        self.assertIs(value["data"]["bridging"], False)
        self.assertEqual(value["data"]["quotePublicId"], "TEST1234")

    def test_reject_unexpected_redirects(self):
        prefix = "https://chat.lemonade.com/gb/home/quote/view?quotePublicId=TEST1234&product=homeowners-gb&bridging=false"
        for url in (None, prefix.replace("https:", "http:"), prefix.replace("chat.lemonade.com", "other.example"), prefix.replace("/quote/view", "/checkout"), prefix + "&quotePublicId=OTHER123", prefix.replace("bridging=false", "bridging=0"), prefix.replace("homeowners-gb", "renters-gb")):
            with self.subTest(url=url), self.assertRaises(StopRun):
                quote_request(url)

    def test_supplied_case_validates(self):
        validate_case(case_fixture())

    def test_bad_input(self):
        for field in ("insured", "postal_code", "property", "compliance"):
            data = case_fixture()
            del data[field]
            with self.subTest(field=field), self.assertRaises(StopRun):
                validate_case(data)

    def test_string_boolean_rejected(self):
        data = case_fixture()
        data["criminalHistory"] = "false"
        with self.assertRaises(StopRun):
            validate_case(data)

    def test_wrong_step_stops(self):
        with self.assertRaises(StopRun):
            answer_for(case_fixture(), 0, {"name": "payment", "status": "pending"})

    def test_not_pending_stops(self):
        with self.assertRaises(StopRun):
            answer_for(case_fixture(), 0, {"name": "user-name", "status": "completed"})

    def test_address_unique(self):
        self.assertEqual(answer_for(case_fixture(), 2, address_step(["Little Haven", "Other house"])), {"addressProviderId": "0"})

    def test_address_no_or_multiple_matches(self):
        for labels in (["Other house"], ["Little Haven 1", "Little Haven 2"]):
            with self.subTest(labels=labels), self.assertRaises(StopRun):
                answer_for(case_fixture(), 2, address_step(labels))

    def test_complete_route_exactly_20_calls_no_checkout(self):
        session = FakeSession()
        with tempfile.TemporaryDirectory() as folder, patch("collect_quote.requests.Session", return_value=session):
            result = collect(case_fixture(), Path(folder))
            self.assertEqual(result["status"], "quoted")
            self.assertEqual(result["request_count"], 20)
            self.assertEqual(list(Path(folder).iterdir()), [])
        self.assertTrue(session.calls[-1][0].endswith("/gb-home-quote-view/sessions"))
        self.assertTrue(all("checkout" not in url for url, _ in session.calls))
        self.assertTrue(all(kwargs["allow_redirects"] is False and kwargs["timeout"] == (10, 60) for _, kwargs in session.calls))

    def test_network_failure_stops_without_retry(self):
        for failure, expected in ((403, "access_denied"), (429, "rate_limited"), (401, "authentication_required"), (500, "technical_failure"), (requests.Timeout(), "pending_timeout")):
            session = FakeSession(failure)
            with tempfile.TemporaryDirectory() as folder, patch("collect_quote.requests.Session", return_value=session), self.assertRaises(StopRun) as caught:
                collect(case_fixture(), Path(folder))
            self.assertEqual(caught.exception.status, expected)
            self.assertEqual(len(session.calls), 1)


if __name__ == "__main__":
    unittest.main()
