# Lemonade: missing-premium investigation results

7 September 2026 | Working proof of concept | Follow-up to the Step A review

## Outcome in brief

**The missing premium has been obtained. The working collector can complete the supplied test case using Python alone.**

Two separate quote journeys for the owner's supplied property and risk answers returned **£51.92 per month**. The first was investigated step by step, viewed in a browser, and then retrieved directly. The second was created and retrieved end to end by the new Python collector without a browser, and subsequently checked in the browser as well.

This worked on the existing Windows host, described by the user as located in Spain. Its public IP geolocation was not independently verified. A UK worker was not necessary for these tests; the package can nevertheless be tried on one.

No checkout was submitted and no policy was purchased. The result is a displayed quote, not confirmation of a bound policy, a final checkout total or a guaranteed annual premium.

## What was wrong, and what fixed it

The original script successfully addressed the questionnaire service but did not know how the final page obtained its data. Downloading the page's initial HTML did not expose its later-rendered price.

The browser revealed a **second script service for viewing quotes**. Calling that service with the quote reference, product and session cookies returned the quote page's structured content—including its main price summary. It did not require rebuilding the questionnaire in a browser or extracting numbers from a large JavaScript bundle.

The working sequence is:

1. Create a questionnaire session and answer its questions using the supplied test case.
2. Read the resulting quote-view link.
3. Extract its quote reference, product and bridging flag.
4. Call the quote-view service within the same Python session.
5. Read the main quote summary, billing period and returned cover configuration; save JSON and CSV.

The browser was valuable as an investigation and verification tool. It is optional—not a normal runtime dependency of the resulting collector. This is the favourable direct-request outcome discussed earlier, demonstrated for this particular journey, not a claim about all insurers.

## Evidence obtained

| Check | Observed result |
|---|---|
| Questionnaire from current host | Session creation and all 18 answer submissions returned HTTP 201 |
| First quote page | Opened successfully; screenshot visibly shows £51.92/mo |
| Browser's quote-view response | Main summary contains £51.92 and period `mo` |
| Direct replay for first quote | HTTP 201 and the same main price, using the pre-browser Python session cookies |
| Fresh direct-only journey | 20 service requests; £51.92/month; approximately 11.26 seconds |
| Browser check of fresh quote | Same displayed price; quote-view response successfully returned |
| Offline tests | 17 tests passed, covering extraction, expected steps, address ambiguity, malformed input, HTTP failures and the bounded complete route |
| Original owner files | SHA-256 checks confirm all three supplied files remain unchanged |

The HTTP count is one session creation, 18 answer submissions and one quote-view session creation. It is **20 requests for one quote**, not one HTTP call per insurance case. Browser page loads make additional asset, analytics and other requests.

Two full quote journeys and one initial empty-session connectivity probe were created. Additional quote-view requests were made for discovery and verification. The account email was generated separately for each full journey; property and risk answers were unchanged. Two matching results for one case are useful reproduction evidence, not statistical evidence of reliability across a portfolio.

## What £51.92 actually represents

The requested cover was buildings and contents. The quote page supplied these defaults:

| Item | Returned/displayed value |
|---|---|
| Supplier brand | Lemonade |
| Displayed premium | £51.92 per month |
| Start date | 8 September 2026 |
| Buildings | Rebuild cost; no fixed monetary limit extracted |
| Contents | £10,000 |
| Temporary accommodation | £20,000 |
| Personal and property liability | £1,000,000 |
| Contents excess | £150 |
| Buildings excess | £150 |
| Escape-of-water excess | £800 |
| Optional packages | Returned switches were off, including home emergency, legal protection, accidental-damage packages and the theft/loss add-on |

The theft/loss add-on being off does **not** mean that burglary cover is absent: the page separately lists burglary among the included perils. This illustrates why internal field names must not be turned into broad coverage conclusions without reviewing the displayed meaning.

These settings were returned by Lemonade; the new collector did not deliberately choose their amounts. The supplier brand and selected cover type have been captured, but the legal underwriting entity has not been separately verified.

Multiplying the monthly amount by 12 would be arithmetic, not a separately quoted annual-payment price. Accordingly, the result leaves `annual_premium` empty for this monthly quote. No independent tax/fee breakdown was extracted.

**The next business question is therefore not merely “can we obtain a price?” but “is this the cover we intend to compare?”**

## The test case and what the owner needs to provide

There was no need to wait for a new case. We used the answers already embedded in the owner's script: the same named applicant, property lookup and household/risk answers. These remain unverified test data; their presence in a working script does not prove representativeness or accuracy.

The script's generated `example.com` email approach was retained. That was accepted in these runs but does not provide a usable mailbox. We did not change answers to improve eligibility or force a cheaper result.

Before broader testing, the owner should confirm:

- That the supplied case and any additional test cases are approved for this use.
- The intended limits, excesses, start-date rule and optional cover to compare.
- A small representative set, including expected variations and non-quote outcomes, plus at least one manually checked quote for like-for-like comparison.

This confirmation is needed for meaningful comparison and repeatable testing—not to establish whether extraction is technically possible, which has now been demonstrated.

## Delivered package

`lemonade-worker-poc-2026-09-07.zip` contains:

- A direct Python collector, external JSON case input, JSON/CSV output and a Windows setup/run guide.
- A separate optional browser observer for later diagnosis.
- Pinned direct dependencies and the 17 offline tests.
- This findings report and a redacted real result.

The normal collector needs Python and Requests. Playwright/Chromium are installed only if the optional browser observer is wanted. The package contains no copied virtual environment, browser binaries, live session cookies, full network captures or active quote link. It does contain the owner's supplied example case so that the recipient can reproduce the same test; circulate it within the intended project team.

The collector checks the exact expected question before submitting each answer, requires one unambiguous address match, bounds its requests, and stops on unexpected questions, access denial, rate limiting or timeouts. It does not automatically retry potentially state-changing submissions. A run that stops writes a non-success result rather than inventing a premium.

## Technical handover

The questionnaire service is:

```text
POST https://chat-api.lemonade.com/chat/public/scripts/gb-home-quote/sessions
POST https://chat-api.lemonade.com/chat/public/scripts/gb-home-quote/sessions/{sessionId}/steps/{stepId}
```

The missing final request, observed in the browser and reproduced directly, is:

```text
POST https://chat-api.lemonade.com/chat/public/scripts/gb-home-quote-view/sessions
```

Its JSON body is:

```json
{
  "data": {
    "quotePublicId": "<reference returned by this questionnaire>",
    "product": "homeowners-gb",
    "bridging": false
  },
  "forceRestart": false
}
```

Use the same `requests.Session` that completed the questionnaire. The successful direct test used ordinary Requests, the accumulated cookies and four explicit headers: Accept and Content-Type as application/json, Origin as `https://chat.lemonade.com`, and Referer as `https://chat.lemonade.com/`. No browser fingerprint imitation or special browser-generated request headers were required in this test. The minimum necessary cookie subset was not investigated; there is no operational reason to discard the working session cookies.

Extract the main summary from:

```text
history[-1].renderedStep.presentation.frame.summary
  price:  "£51.92"
  period: "mo"
  type:   "price"
```

Returned defaults are in `history[-1].renderedStep.data.values`. Do not search for the first pound amount in the whole response: it also contains add-on prices and cover limits. The quote step is marked `pending` because the user can proceed towards checkout; in this observed response that does not mean the displayed premium is still being calculated.

The original email-security URL wrappers were replaced with their actual HTTPS addresses in the new code only. The original file was preserved. This is an observed website-internal interface, not a published partner API or a promise of continued compatibility.

## Remaining work and stopping point

The missing-premium investigation reached a useful result well inside the eight-hour ceiling. There is no reason to consume the rest of the allowance on speculative browser work now that the direct route is demonstrated.

This is not yet a production batch worker. Untested areas include different questionnaire branches, declines/referrals, recurring use of the same cases, sustained volume, deliberate selection of comparable cover, recovery after interruptions, UK-host behaviour and Linux execution. The code stops safely on unsupported branches; it does not yet understand and label every insurer business outcome.

The next useful increment is to agree cover settings and validate a small owner-approved set against manual quotes. Batch scheduling, Portal integration and longer-term monitoring can then be scoped using those results. A UK comparison test remains available if needed, but is not a blocker for continuing on the current host.
