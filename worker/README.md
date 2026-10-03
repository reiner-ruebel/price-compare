# Lemonade UK: single-case quote test

## What this package does

Submits the questionnaire answers in `case-owner-example.json`, obtains the quote reference, and retrieves the displayed premium and default cover settings. It stops at the quote: it does not enter checkout or buy insurance.

On 7 September 2026 the supplied example returned **GBP 51.92 per month**. A complete run using Python Requests alone took approximately 11 seconds on the existing Windows host, described by the operator as located in Spain. That is an observation, not a speed or availability guarantee. A browser was used to discover and verify the response; it is **not required by the collector**.

Read `FINDINGS.md` in the ZIP for the investigation and limitations. `sample-result.json` is a redacted real result, not a price prediction for a future run.

## First run on Windows

Tested with Python 3.12.14. Install an IT-approved Python 3.12 if it is not already available. Extract the whole ZIP into a normal writable folder. Open PowerShell in that folder and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s . -p test_collect_quote.py -v
```

Those tests are offline and do not contact Lemonade. No browser, IIS, database, cloud account, or extra Windows machine is required by this collector. It can also be tried on a UK worker with the same setup; no UK worker was needed for our successful runs.

Review the input file, then deliberately start one live test:

```powershell
.\.venv\Scripts\python.exe collect_quote.py --confirm-test-submission
```

The confirmation flag authorises this run to submit the test's questionnaire and account-details answers. The supplied flow includes agreement-to-terms set to true and marketing consent set to false. A blank `email` generates a unique address at `example.com`, as in the owner's original test approach; it is not a usable mailbox. Do not put an unrelated person's real email there. These are real requests to the live service, not a sandbox simulation.

Expected final output for a successful case:

```text
Result: quoted 51.92 GBP month
Saved: ...\runs\<new-run-folder>
```

The amount may change. If the result is not `quoted`, read its `detail` field. Do not repeatedly rerun a blocked case. Exit code 0 means a recognised quote was extracted; 2 means the run stopped or failed.

## Input and results

- `case-owner-example.json`: transcribed from the supplied script. The owner still needs to confirm that this is an approved, representative test case. No different property or favourable risk answers were invented during the investigation.
- `runs/<run-id>/result.csv`: one result row, suitable for opening in Excel.
- `runs/<run-id>/result.json`: the result plus returned limits, excesses, cover switches, start date, quote reference and input-file fingerprint.

Each invocation creates a new folder and a new test journey. It does not resume an interrupted application or overwrite a previous result. An explicit output folder must not already exist:

```powershell
.\.venv\Scripts\python.exe collect_quote.py --case .\my-approved-case.json --output .\runs\uk-test-001 --confirm-test-submission
```

This is a single-case prototype, not a general insurance questionnaire engine. It supports the observed homeowner/buildings-and-contents sequence. If different answers produce additional questions, it stops rather than guessing. It does not yet select target cover amounts, a specified start date or excesses. Instead, it records the defaults returned by Lemonade. Use the JSON when assessing comparability; the compact CSV alone is insufficient for that.

## Optional browser diagnosis

Use only if a developer needs to inspect the quote page. Install the separate browser dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-browser.txt
$env:PLAYWRIGHT_SKIP_BROWSER_GC = '1'
.\.venv\Scripts\python.exe -m playwright install chromium
```

Create one diagnostic run:

```powershell
.\.venv\Scripts\python.exe collect_quote.py --confirm-test-submission --save-private
.\.venv\Scripts\python.exe observe_quote.py .\runs\<the-new-run-folder> --headed
```

The observer loads only the resulting quote page and watches its requests; it does not click checkout. Browser diagnosis requires `state.private.json`, which is only saved after the questionnaire reaches a quote redirect. It cannot diagnose an earlier incomplete journey by itself.

`--save-private` writes full service responses and session cookies locally. Browser observation also saves network details, page text and a screenshot. Treat those files as confidential session material and share them only through an agreed secure channel. They are deliberately excluded from this delivery ZIP. Ordinary collection does not save cookies or full responses.

The code uses ordinary Requests and optional ordinary Playwright. It includes no proxy rotation, fingerprint spoofing, CAPTCHA solving or challenge-bypass logic.

## Scope and next step

The connection to the site's private web-application service is observed behaviour, not a documented or guaranteed partner API. Two quote journeys for the same property/risk answers succeeded; other cases, later dates, Linux and a UK host have not been tested. Owner-approved representative cases and agreed cover settings are the next useful input. Batch processing, scheduling, Portal integration and production support are not included in this package.
