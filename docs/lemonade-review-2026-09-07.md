# Lemonade UK quote automation: review and proposed next step

Date: 7 September 2026  
Audience: project owner and technical implementation team  
Effort: one person-day (MD) means eight working hours

## 1. Decision in brief

**Yes, this is a credible problem to investigate and likely a useful extension of the owner's existing work. I would accept a one-day investigation. I would not promise a completed, reliable quote collector within that day.**

The owner reports that the questionnaire produces a quote identifier, but the script cannot obtain the premium displayed afterwards. A browser loading extra data after the initial HTML response is a normal application pattern. Playwright can observe those requests and the rendered result. This offers a concrete route forward without immediately rebuilding the questionnaire.

There are two separate findings:

- The supplied copy has email-security URL wrappers in its service address and headers. These need correcting before it can be used as an executable baseline. They may have been introduced when the code was shared, rather than being present in the owner's working copy.
- The missing quote retrieval remains unproven. Finding a request does not establish that it can be replayed using only a quote ID: cookies, other tokens, browser storage, or several requests may also be required.

My preferred sequence is to preserve the existing questionnaire logic, observe the final page in a normal browser session, and then choose between direct retrieval and a small browser-assisted finishing stage. Rebuild the entire journey in Playwright only if reproduction shows that this is necessary.

**Evidence boundary:** this report is a source review, an offline syntax/structure check, and a limited public-page reachability check. No quote was created, no account details were submitted, and no premium was extracted during this review. The owner's reported successful runs have not been independently reproduced. The original script has not been modified.

## 2. What was provided and what is established

| Material | What it establishes |
|---|---|
| [task.txt](../task.txt) | Request to spend a day investigating the Lemonade issues |
| [internal-comments.txt](../internal-comments.txt) | Owner reports successful onboarding, a quotePublicId, a quote-view URL, and an unresolved premium-fetch request |
| [Lemonade_text.py](../Lemonade_text.py) | A concrete exploratory questionnaire script, followed by HTML and JavaScript inspection |
| [Legacy worker discussion](D:/repos/price-compare-and-more/docs/worker.md) | Earlier manual, scheduled and Portal-operated worker architecture |
| [Legacy decision-paper draft](D:/repos/price-compare-and-more/matrix/price-comparison-decision-paper-v3-draft.md) | Earlier staged pilot approach and success definitions; broader scope than this one-day request |

The designated final legacy document remains at [price-comparison-decision-paper-v1.pdf](D:/repos/price-compare-and-more/output/pdf/price-comparison-decision-paper-v1.pdf). Its existence was verified; it was not rewritten or used to infer current Lemonade behaviour. This review uses the supplied source and comments as the current technical evidence.

The new folder initially contained only the three owner files. There was no saved quote response, quote-page HTML, downloaded application bundle, HAR network capture, case batch, dependency manifest, or known premium to verify. The script contains commands that would produce several of these files, but the generated files were not supplied.

Offline inspection established:

- Python syntax parses successfully: no syntax repair is needed before the structural fixes.
- 1,183 source lines, with no function definitions: this is a sequential exploratory script.
- 22 HTTP call sites: 19 POSTs and three GETs. None supplies an explicit timeout. This count is not the complete request count of a browser journey.
- A Requests session is used, which is a useful foundation for preserving cookies between calls.
- The answers describe one fixed case and one sequence of questions. This does not establish coverage of alternative household/property circumstances.
- There is no implemented premium extraction or structured quote-result export.

An identifier and a successful HTML response are intermediate milestones. They do not alone prove that an offer exists, is ready, is accessible to the session, or has a particular premium. Those claims require the actual result page or response.

## 3. Key code observations

Line references refer to the unchanged supplied file.

| Observation | Evidence | Consequence and proposed action |
|---|---|---|
| Service URL is wrapped by email security | Lines 5, 21-25 | The first POST is addressed to `urldefense.com`, with `/sessions` appended to the wrapper. Restore the actual Lemonade service URL before execution. |
| Origin and Referer are also wrapped | Lines 12-13 | These headers describe the wrong website and contain trailing spaces. Restore the actual origin and referer expected for the observed flow. |
| Application bundle URL is wrapped and fixed to a release filename | Line 977 | Both the wrapper and the hard-coded asset name can invalidate inspection. Discover the scripts loaded by the current page. |
| Responses are mostly parsed before validation | First example: lines 27-38; repeated throughout | An HTML error, denied request, or changed JSON shape causes misleading JSON/key errors. Check status, content type, error fields and expected structure before advancing. |
| No explicit request timeouts | All 22 call sites | A run can stall. Add connect/read timeouts and a bounded total wait for pricing. Retry only where the operation is safe to retry. |
| Next step assumed to be the last history entry | Repeated `history[-1]` | Validate the expected step name/type and pending status. Stop with a useful reason on an unrecognised branch rather than applying the next hard-coded answer. |
| Variables are assigned only on HTTP 201 paths but used afterwards | Lines 746-772, 797-826, 865-895 | Failure may leave a variable undefined or reuse stale `next_step` data. Handle each response as an explicit success, pending, referral/decline, or failure. |
| One fixed set of answers and an address substring selection | Lines 64-71, 160-188 and subsequent payloads | Suitable for a reference case, not a general batch. Later introduce input records, unambiguous address matching, and handlers for supported question variants. |
| Final URL is handled by removing quote characters | Lines 895-906 | Validate the actual response shape; resolve relative URLs against the correct origin; check expected host/path before navigation. Do not assume removing characters is a general decoding rule. |
| First discovered script is assumed useful | Lines 928-945 | A first script may be analytics or a loader. Relative asset paths also need resolution. Browser network observation is more informative than keyword counts in one bundle. |
| Cookies and raw responses are printed | Examples at 554-555, 743-744, 1141-1143 | Logs can expose session credentials and case data. Keep diagnostic metadata and redacted excerpts; restrict any short-lived raw capture. |
| Debug files have fixed names in the working directory | Lines 915, 950, 984, 1149 | Subsequent runs overwrite evidence. Use a directory per run/case and a clear output file. |

The direct addresses visible inside the wrappers are:

```text
Service base: https://chat-api.lemonade.com/chat/public/scripts/gb-home-quote
Origin:       https://chat.lemonade.com
Referer:      https://chat.lemonade.com/
```

These are recovered from the owner's text, not verified current API contracts. The old bundle filename should not become a permanent configuration value.

The script also submits account details and sets `termsOfServiceApproved` to true. It is therefore not a passive page reader. Controlled runs should use the owner's designated artificial case/contact arrangement, preserve the intended answers and stop at the quote, before purchase. Do not change insurance answers to force a price. A referral or decline is a valid business outcome.

## 4. How I would investigate and fix the missing premium

### Step A: establish a usable reference run

Correct the URL wrappers in a working copy and add the minimum status/step checks needed to locate failure accurately. Confirm the owner's reference case, the expected terminal response and the exact quote URL. Retain the session in memory. Compare against a manually visible result from the same case and environment.

A recent network capture from the owner's successful environment would accelerate this considerably. It should include the quote-loading request and its response, with sensitive session material exchanged only through a controlled channel if needed for short-lived debugging. A standalone quote ID may be insufficient or expired.

### Step B: observe the quote page

Attach network listeners before navigating to the returned URL. Observe Fetch/XHR requests, redirects, browser errors and rendered text. If the result is not in those responses, inspect initial page data and any other relevant transport, such as WebSocket messages. Wait for an identified quote-ready condition rather than a fixed sleep.

Locate a response that can be tied to this specific quote and explains the visible premium. Identify currency, annual/monthly basis, excess, cover selections and any tax/fee information actually returned. Do not choose the first numeric field called `price`: it could be an add-on, an old value, a default example or one instalment.

Playwright officially supports observing browser HTTP requests and responses, including Fetch/XHR. [Network documentation](https://playwright.dev/python/docs/network)

### Step C: choose the smallest working retrieval method

| Observed behaviour | Implementation choice |
|---|---|
| A request returns quote data using the existing session and a reproducible payload | Keep Requests for onboarding and add direct quote retrieval. Playwright may be needed only during diagnosis. |
| The result requires browser initialisation but is then exposed in a response or the page | Retain the questionnaire and use Playwright for the final stage, preserving the required session state. |
| Moving between Requests and the browser loses required state | Consider making the API calls through a Playwright browser context's request client, which shares its cookies, or operate more of the flow through the browser. |
| The session cannot be resumed reliably outside the full browser journey | Implement a browser journey; estimate this separately once the failing stage is understood. |
| No usable quote can be reached from the available environment | Return an evidence-backed blocker and use the owner's working environment or capture to distinguish access problems from extraction problems. |

Requests and Playwright do not automatically share a session. Cookie transfer must preserve domain, path, expiry and security attributes. Cookies also do not necessarily contain all application state: tokens in page storage or bootstrap data may matter. A Playwright context's HTTP request client shares cookies with its browser context, but remains an HTTP client; it does not make every API call execute as browser JavaScript. [APIRequestContext documentation](https://playwright.dev/python/docs/api/class-apirequestcontext)

The quote endpoint is **not identified in this review**. No URL pattern or authentication requirement should be invented and treated as established.

### Step D: prove the result

For a narrow successful repair, deliver a command that processes the agreed reference case and writes a structured result with case ID, run ID, timestamp, quote ID, status, product/brand, price, currency and payment period. Include excess/cover details where reliably available. Record missing values explicitly.

Verify that the extracted result matches the same quote in the browser, then repeat with a fresh isolated session. A monthly amount multiplied by twelve must not silently be reported as an offered annual payment price. A failure must not become a zero premium or another case's previous result.

## 5. What I would buy with the first day

The one-day request is a smaller diagnostic intervention than the earlier 10 MD pilot. It can benefit from the owner's existing progress without committing to the broader pilot scope.

| Activity | Budget within 1 MD | Expected evidence |
|---|---:|---|
| Correct received configuration and reproduce the reference path | 1.5 hours | Exact stage reached and useful failure output |
| Observe browser quote loading and identify state/data dependencies | 3 hours | Relevant request/response or a specific blocker |
| Try direct retrieval or a minimal browser-assisted extraction | 2 hours | Working extraction if feasible, or tested explanation of why not |
| Compare with the visible quote, package findings and next estimate | 1.5 hours | Result evidence, working changes where achieved, and handover |
| **Total** | **8 hours / 1 MD** | **A bounded attempt with a useful decision** |

This is a proposed work budget, not a claim that this review consumed a full day. If initial reproduction fails, the remaining time goes into isolating that failure and obtaining useful evidence; it does not disappear into unrelated product features.

At the end of the day, I would accept either a verified premium retrieval for the reference case, or a precise unresolved dependency supported by observations. I would not accept only another list of guessed endpoint names.

Indicative follow-on allowances, based on engineering judgement rather than a measured implementation:

| Scope | Additional effort after the first day | Conditions |
|---|---:|---|
| Finish a straightforward extraction and hand over a repeatable single-case script | 0-2 MD | The owner-reported onboarding still works and the retrieval is simple |
| Stabilise a browser-assisted finishing stage and its session handling | 2-4 MD | Alternative to the simple retrieval allowance, not automatically additive |
| Replace the complete questionnaire with a browser journey | 4-8 MD | Alternative implementation branch; only if needed; access remains unguaranteed |
| Add file-driven batch processing for agreed case variants, isolation, recovery and normal output checks | 3-6 MD | After a working extraction; scope depends on the actual test cases |
| Install on one agreed worker and demonstrate a scheduled run | 0.5-1 MD | Machine/network/account already available; overlaps with setup work already completed |
| Later Peril Manager job submission, worker polling, results import and shared views | 5-10 MD provisional | Separate optional scope; current Portal code needs a focused review before commitment |

These are branches and extensions, not a list to add together indiscriminately. For the current request I would authorise only the first 1 MD, then review the evidence. Normal developer testing belongs in these estimates. Broad edge-case campaigns, scale testing and additional targets can be commissioned on demand; correct results, case isolation and explicit failures remain basic requirements.

## 6. Proposed components if implemented

Start with a small Python command-line application. No database, web server or Portal deployment is required to solve the immediate retrieval problem.

```text
Input case file
  -> runner: validate input and create isolated run
  -> Lemonade questionnaire adapter
  -> quote reader: direct HTTP or Playwright-assisted
  -> normaliser and result checks
  -> result.json / results.csv plus bounded diagnostic evidence
```

Suggested responsibilities:

- `runner`: input/output paths, one run per invocation, exit status and total timeout.
- `lemonade_onboarding`: session management, request validation and supported question handlers.
- `lemonade_quote`: validated redirect, quote-ready wait, retrieval and quote-ID correlation.
- `results`: typed fields, monetary units, payment basis and CSV/JSON writing.
- `diagnostics`: redacted stage logs, selected response metadata and optional screenshot.
- Later `worker_agent`: obtains jobs from Peril Manager, invokes the same runner and uploads results.

Maintain one outcome per attempted case. Useful outcomes include `quoted`, `declined`, `referred`, `challenged`, `access_denied`, `unexpected_step`, `quote_pending_timeout` and `technical_failure`.

For Portal operation, use outbound HTTPS from the worker to an authenticated job API. Peril Manager manages users, input artifacts, job status and result tables; the worker runs the quote journey locally. Hosting the Portal in Spain does not make a German or UK worker's browser traffic originate in Spain. A worker that calls through a proxy, however, presents the proxy's exit network.

The earlier Foundation/FastAPI bridge is background context, not evidence that this connector already exists. A remote worker pulling jobs and an internal FastAPI service called by the Portal are distinct deployment arrangements.

## 7. What must be installed on a worker

| Component | When needed |
|---|---|
| Supported Windows or Linux installation | Existing host is sufficient; a VM is optional |
| Supported Python, preferably a maintained 3.12/3.13 environment after dependency validation | Always |
| Dedicated Python virtual environment and pinned dependency file | Always for reproducible installation |
| `requests` | To retain the supplied direct HTTP approach |
| `playwright` Python package and its Chromium browser download | Diagnosis and any browser-assisted runtime |
| Browser operating-system dependencies | Especially Linux; install for the chosen Playwright/browser version |
| Writable input/output/log folders under the execution account | Always |
| Task Scheduler on Windows or a systemd service/timer on Linux | Optional unattended operation |
| Worker credentials and Portal URL | Optional Portal integration |

JSON and CSV support are built into Python. Excel support would add a package only if XLSX input/output is chosen. Selenium is an alternative to Playwright, not an additional requirement. A separate Node.js project, IIS, SQL Server, Docker, and a paid browser-automation service are not required for this runner. The Playwright Python installation supplies its driver; Chromium is a separate install step.

Illustrative Windows setup after choosing an installed Python interpreter:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install requests playwright
.\.venv\Scripts\python.exe -m playwright install chromium
```

The delivered package should use validated pinned versions. Install and smoke-test the browser under the account that will run the scheduled task. On supported Linux distributions, Playwright can install Chromium and its dependencies with `python -m playwright install --with-deps chromium` (system dependency installation can require administrator privileges). [Playwright library setup](https://playwright.dev/python/docs/library)

Current Playwright documentation supports Windows 11 and supported Windows Server versions, as well as named Ubuntu/Debian releases. Select a supported distribution rather than treating every Linux distribution as interchangeable. [System requirements](https://playwright.dev/python/docs/intro#system-requirements)

For one browser at a time, a starting allocation of two CPU cores, 4 GB RAM and several GB of free storage is a planning assumption to measure, not a certified capacity requirement. Existing machines may need no hardware purchase. Linux avoids a Windows licence but still needs hosting or a physical computer, updates and maintenance.

On this host, the bundled Python 3.12.14 runtime was available, but `requests` and `playwright` were not installed in that runtime. This is not an inventory of every Python environment on the machine. No worker dependencies were installed during the review.

## 8. Germany, Spain and a UK worker

The countries and hosting arrangements below come from the user. Public exit IPs, VPN routing and provider classifications were not independently established.

| Environment | Expected implications | Recommended role |
|---|---|---|
| Windows 11 PC in Germany | German exit address unless routed elsewhere. Household/office classification depends on its ISP and VPN, not Windows. It may work, be redirected or encounter restrictions. | Good for development and visible-browser diagnosis; a failure here does not prove UK infeasibility. |
| Leased server in Spain | Likely hosting-provider network; Spanish exit if routed directly. Different client/network characteristics may affect acceptance. Physical server location does not prove observed IP location. | Code preparation, offline tests and controlled diagnosis. Do not assume it is the production quote worker. |
| Owner-managed UK office/household worker | UK network and a locally typical usage environment. Still no guarantee of quote eligibility or automated access. | Useful reference and candidate operating environment. |
| UK cloud Linux/Windows worker | UK exit country, usually recognisable as hosting infrastructure. Country and network class are separate factors. | Candidate for unattended operation after target-specific verification. |

There is already one concrete local observation: on 7 September, a plain Python `urllib` GET to `https://www.lemonade.com/gb/home` returned HTTP 403. A second diagnostic GET returned the same status with `Server: cloudflare` and body `error code: 1010`. Cloudflare documents 1010 as rejection based on the client's browser signature. [Cloudflare error 1010](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/)

That observation concerns the public landing page with a default Python client from this host. It does **not** establish a Spain geoblock, failure of the separate chat API, rejection of every Python client, or the behaviour of an ordinary browser. There were no quote submissions in these checks and no attempts to bypass the denial.

The correct comparison is the same approved test case, software version and browser mode across environments, recording the stage reached, status, timing and result. First establish a manual reference in the owner's known-working environment. Do not attribute an error to geography until client, session and request differences have been considered.

A useful arrangement is to develop and maintain the code on the Spain server while executing the diagnostic package on the Germany PC or the owner's UK machine. Only a successful run on the intended operating worker demonstrates readiness for that environment. This session has no verified remote execution connection to the Germany PC.

## 9. Project housekeeping and next decision

The app's project inventory on 7 September already lists a standard local project named `price-compare`, pointing to `D:\repos\price-compare`. This task, `ERGO Price Comparision`, is associated with that exact project and folder. The project is not currently a Git repository; Git is a separate development choice, not a missing project association.

The old `price-compare-and-more` folder and its final PDF still exist. No unrelated material was moved into the new project. The previous "moved or deleted" label is not present in the current project inventory; its former visual state was not reproduced. There is no need to recreate this task or edit app storage to repair the current association.

The immediate next implementation package should be the one-day Lemonade investigation described above. The best supporting inputs are a fresh successful owner run/capture, a manually visible premium for the approved reference case, and the intended execution environment. These help resolve the remaining uncertainty; they do not prevent the source-level assessment delivered here.

### Source preservation record

SHA-256 of the three supplied files, before review and verified unchanged at handover:

```text
task.txt
306F98614647D6B0CFD3B4E638F2C8E22D98D992A1B04E39C0A5E7B3CFEE9E0C

internal-comments.txt
2CF33E02F334F7FBD0036498C0808F6CE92664CB055AE17360CE8AD0749E5319

Lemonade_text.py
6F39F34CAACBAFC29428923CB91A60380176A6FB78EFB845EA1B7FA4875A8AFE
```
