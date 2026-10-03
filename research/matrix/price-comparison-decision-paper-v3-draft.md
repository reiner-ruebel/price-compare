# Household Insurance Price Comparison

## A controlled pilot and an evidence-based route to an operational service

**First discussion draft - Version 1**  
**Prepared for:** ERGO UK and Ireland  
**Date:** 27 July 2026  
**Effort unit:** one person-day (MD) = eight working hours

> **The proposed purchase is a 10 MD pilot, not a complete four-target system.**
>
> The pilot uses the owner's test cases, one selected target website and a controlled UK worker - a dedicated computer located in the target market that runs the quote journeys (see Section 07). It produces actual results and enough evidence to decide whether to continue, change target or stop. A second 10 MD round is commissioned only if the first result justifies it.

---

## 01 | Executive summary

### The opportunity

The owner wants to observe household-insurance prices for a stable set of approximately 250 test cases. The intended weekly scope is one comparison portal and three direct competitors:

`250 test cases x 4 target websites = approximately 1,000 quote journeys per week`

The cases are artificial test cases owned and maintained by the owner. They are not customer cases. Their values may change without changing the size or structure of the test set.

A comparison portal can return offers from a broad panel in one journey. Direct-insurer journeys can then add or verify selected competitor positions. This can provide useful pricing intelligence, but it does not guarantee complete market coverage or directly comparable products.

### The honest technical position

There is no single technical method that can be assumed to work for every target or to keep working indefinitely.

The supplied German example sends requests directly to a target system. That can be efficient when a suitable and stable request route exists. Other targets may require the solution to work through a browser. Target journeys, access controls and product questions can change. A working target may therefore require maintenance later even when the owner's cases have not changed.

The practical approach is to learn in controlled steps:

1. start with the simplest appropriate method;
2. move to a browser-based journey if necessary;
3. make the working journey operational and observable;
4. repair or replace a target when continued use no longer produces reliable results.

The work does not include defeating access controls, solving CAPTCHAs or disguising the solution as a human user.

### Recommendation

Buy one **10 MD pilot** with:

- one agreed UK target;
- the owner's test-case file;
- a controlled UK worker (a dedicated computer located in the target market; see Section 07);
- a result for every attempted case;
- price plus insurer/product name for each successful quote;
- a manual reference sample for checking result correctness;
- measured run time, failure reasons and observed restrictions; and
- a written continue/change/stop recommendation.

Do not commission the complete four-target solution before this evidence exists.

For later operation, **Peril Manager v-11 is the preferred control and reporting option** when the owner wants managed imports, shared results, history, filtering and audit. The quote journeys should still run on a separate controlled worker rather than on the existing application/database sandbox server.

If the pilot is promising, buy a second **10 MD delivery round**. Its purpose is selected at the pilot review: improve the first target, add a second target, move from direct requests to a browser journey, or prepare reliable weekly operation.

After 20 MD, the owner should have a materially better basis for selecting targets and estimating the next twelve months. Before then, a precise annual delivery or maintenance forecast would suggest certainty that does not yet exist.

### What the owner must decide

| Decision | Proposed starting position |
|---|---|
| Pilot country | United Kingdom |
| First target | One comparison portal, selected for result value and technical feasibility |
| Test data | Approximately 250 owner-supplied artificial cases |
| Minimum result | Price plus insurer/product name; a status for every attempted case |
| Worker | One dedicated, managed UK virtual machine |
| Pilot effort | 10 supplier MD |
| Review | Continue, change target/method, or stop |
| Further commitment | One additional 10 MD round only after review |

---

## 02 | What is being bought

### Round 1 - controlled pilot: 10 MD

The pilot is a working technical and business test, not a paper study and not a throwaway demonstration.

An indicative sequence is:

| Pilot activity | Indicative effort | Result |
|---|---:|---|
| Confirm target, input, result and success definitions | 1 MD | Agreed pilot brief and owner decisions |
| Manual reference journey and field mapping | 1 MD | Known questions, answers and expected result |
| Test the simplest appropriate access method | 2 MD | Early feasibility result; method is time-boxed |
| Build or adapt the working target journey | 3 MD | Runnable one-target translation |
| Batch input, normalized output and basic diagnostics | 1 MD | Repeatable case processing |
| Representative/full run and correctness checks | 1 MD | Actual owner-case results and comparison evidence |
| Decision paper, handover and next-round estimate | 1 MD | Continue/change/stop recommendation |
| **Total** | **10 MD** | |

The sequence can change when the target requires it. The 10 MD is a time-box: the owner buys evidence and a working result where feasible, not an unconditional promise that any selected website can be automated.

### Pilot deliverables

The owner receives:

- the runnable one-target pilot;
- the target-specific translation created during the pilot;
- the agreed input and result formats;
- the result file from the agreed pilot run;
- a status and reason for every attempted case;
- price and insurer/product name for successful quotes;
- a small manual-versus-automated reference check;
- measured run time and completion rate;
- a list of fields or cases that need an owner decision;
- observed access restrictions and operational risks;
- concise operating instructions; and
- a recommendation and estimate for the next 10 MD round.

The code is retained and reused if work continues.

### Round 2 - selected after the pilot: 10 MD

The second round is deliberately not fixed in advance. It should address the most valuable next constraint observed in Round 1.

Possible Round 2 outcomes include:

| Scenario after Round 1 | Sensible use of Round 2 |
|---|---|
| Direct requests work reliably | Make the first target operational and add a second target |
| Direct requests are not suitable | Implement the first target through a browser journey |
| The target is unsuitable | Select and build a better first target |
| Results are available but incomplete | Improve extraction and product comparability |
| The journey works but weekly operation is fragile | Add scheduling, restart, monitoring and operating controls |
| The business value is not demonstrated | Stop without commissioning further work |

### What is not being bought at the start

- a guarantee that all four preferred targets can be automated;
- a promise that a working journey will never require maintenance;
- unrestricted operation from many employee PCs;
- automatic bypass of CAPTCHA, authentication or access restrictions;
- a complete Peril Manager v-11 integration;
- exhaustive edge-case and adversarial testing;
- a legal opinion on the use of target websites; or
- a fixed twelve-month maintenance commitment before the pilot evidence exists.

---

## 03 | Defining success before development

“The system produced a result” can mean several different things. The owner should decide which level is needed.

| Level | What the result contains | Business value |
|---|---|---|
| **S0 - Technical status** | Completed, declined, referred, challenged or failed | Shows whether the journey can be operated, but does not yet provide a quote |
| **S1 - Minimum price result** | **Price plus insurer/product name**, with case, target and time | Proposed minimum useful result |
| **S2 - Comparable quote** | S1 plus payment basis, excess, cover type and selected material options | Supports a more defensible price comparison |
| **S3 - Evidence and analysis** | S2 plus evidence, history, ranking and change reporting | Supports review, audit and recurring pricing analysis |

### Proposed pilot acceptance basis

For this draft, the pilot is designed around **S1**. The result file should contain:

- owner case identifier;
- target and run identifier;
- date and time;
- journey status;
- insurer and product name;
- quoted price and payment period;
- failure or no-quote reason where available; and
- technical diagnostic reference.

The owner should confirm before work starts:

1. whether a portal should return only the leading offer or every returned offer;
2. whether annual price is sufficient or monthly instalments and finance cost are also required;
3. how insurer, brand, product and underwriter should be distinguished;
4. whether a quote without excess and cover details is genuinely useful; and
5. how declined, referred and manually reviewed cases should appear.

### How correctness should be judged

A high technical completion rate is not enough if the extracted price is wrong. The pilot should therefore use a small manually executed reference set.

The provisional quality tests are:

- every attempted case has an interpretable status;
- every successful quote has price plus insurer/product name;
- automated results agree with the manual reference for the agreed fields, allowing for legitimate quote changes between runs;
- repeated cases do not silently inherit data from earlier browser sessions; and
- exceptions are visible rather than being converted into plausible but wrong prices.

The manual reference establishes the denominator before a percentage threshold is agreed. This avoids treating a legitimate target decline as an automation failure.

---

## 04 | The competitive landscape

### United Kingdom

The UK is the better starting market because comparison portals expose broad panels and public online quote journeys.

The Association of British Insurers reported an average combined buildings-and-contents premium of **£395 in 2024**. Its property tracker analyses **16.5 million policies sold per year**. This indicates a large and active market, but it does not mean that any one portal provides complete market coverage.

Current public portal statements illustrate the breadth and the overlap:

| Portal | Publicly stated position | Interpretation for the pilot |
|---|---|---|
| MoneySuperMarket | Compares prices from 103 UK home-insurance providers | Broad result opportunity; provider and product variants must be grouped carefully |
| Go.Compare | 82 active home insurers on its panel as at 6 July 2026 | Broad panel and a strong portal candidate |
| Confused.com | Lists 83 home-insurance companies, correct as at April 2026 | Transparent public list is useful for target and brand mapping |
| Compare the Market | Major current household quote journey | Tier-one candidate even without a directly comparable public panel count in the reviewed material |

These numbers are the portals' public descriptions. They are not counts of independent underwriters, and their panels can change.

Candidate direct targets visible across current UK portal material include Admiral, Allianz, Aviva, AXA, Churchill, Hastings, LV=, Policy Expert and Tesco Insurance. The final direct targets should not be chosen by brand recognition alone. They should be selected after considering:

- frequency and relevance in the owner's test scenarios;
- distinct insurer/underwriter and product position;
- result value beyond the selected portal;
- product comparability;
- public journey stability; and
- technical and compliance feasibility.

### Republic of Ireland

The Irish comparison market is narrower and should not simply copy the UK design.

Insurance Ireland's 2024 Factfile reports **EUR 657.5 million** of household gross written premium. The 2022 Census recorded approximately **1.85 million occupied dwellings**.

Public comparison evidence is more limited:

| Service | Publicly stated position | Interpretation |
|---|---|---|
| bonkers.ie | Home policies available from Aviva and Zurich | Useful journey, but not a broad whole-market panel |
| Chill | Panel of 14 insurers across its product offering | Home subset and result mechanics require a pilot check |
| Compare Insurance Ireland | Names examples including Aviva, Zurich, AXA, Allianz and AIG | Confirm whether each journey returns comparable online prices or broker follow-up |

For Ireland, one portal/broker journey plus selected direct insurers may still be useful, but direct journeys are likely to add more incremental coverage than in the UK.

### Competition conclusion

Start with one UK portal. A portal offers the highest potential information return from one translation. Select direct competitors only after the portal result shows which brands, products and coverage gaps are most relevant to the owner's test cases.

This sequencing is more valuable than fixing all four targets before any real result has been observed.

---

## 05 | How to work with effort

### Use evidence gates, not a large up-front estimate

Target websites are external systems outside the supplier's control. The right estimate becomes clearer only after real journeys have been built and run.

The recommended commercial rhythm is:

`10 MD pilot -> review -> 10 MD next constraint -> review -> twelve-month plan`

Each review answers four questions:

1. Are the results useful?
2. Are they correct enough for the intended decision?
3. Can the target be operated at the required volume and location?
4. Is the next improvement worth its effort and operating risk?

### Indicative later effort - not an initial commitment

After a stable pattern exists, a further target may take:

- **2-4 MD** when a suitable direct request route exists;
- **5-10 MD** for a normal browser-based quote journey; or
- more where the journey is unusually long, unstable, protected or materially different.

A target change is not a complete rebuild. Shared input, output, scheduling and reporting components are retained; the target-specific translation is replaced or repaired.

After the first two rounds, a twelve-month maintenance plan can be assigned to an observed scenario:

| Observed scenario | Indicative planning range | Meaning |
|---|---:|---|
| Stable targets | 12-24 MD/year | Periodic checks and small repairs |
| Normal external change | 24-48 MD/year | Several journey or extraction changes across live targets |
| Difficult/restrictive targets | 48-80 MD/year | Repeated redesign, deeper checking or target substitution |

These ranges are planning bands, not a maintenance quote. A difficult target should be replaced when its information value no longer justifies the effort.

### Edge testing on demand

The first version should include normal development tests and representative end-to-end checks. Exhaustive testing of unusual combinations can be added when the owner has evidence that it is valuable.

On-demand assurance can include:

- uncommon property and cover combinations;
- long-running recovery and soak tests;
- stronger wrong-result detection;
- extended screenshots or response evidence;
- detailed rate and traffic controls;
- formal security/privacy assurance; and
- deeper product-comparability rules.

---

## 06 | Peril Manager v-11 option

### Why it is relevant

The pilot can operate with protected input and result files. If the owner wants a shared operational service, Peril Manager v-11 can provide the surrounding business application without rebuilding functions that already exist.

Peril Manager v-11 can provide:

- controlled test-case imports;
- online view and editing;
- shared files and access control;
- persisted run and result tables;
- filtering, queries and aggregates;
- result history and exports;
- request/result audit; and
- visible operational status.

The target journeys still run on the separate controlled UK worker. Peril Manager v-11 becomes the control, storage and reporting layer; the worker performs the external browser or direct-request activity.

### Recommended timing

Do not integrate the pilot into Peril Manager v-11 before one target has proved that it can return useful results. The pilot first establishes the real input, output, status and diagnostic artifacts.

After that proof, a **10 MD integration round** is a reasonable planning allowance for:

- Foundation table and artifact definitions;
- import and export;
- view, edit and access rules;
- job submission and status;
- persisted normalized results;
- filters, queries and basic aggregates;
- audit references; and
- deployment into the agreed Peril Manager environment.

The estimate should be confirmed against the actual pilot artifacts. This integration does not replace or rewrite target-specific translations.

### Preferred operational shape

| Component | Responsibility |
|---|---|
| Peril Manager v-11 | Users, imports, jobs, result storage, review, reporting and audit |
| Controlled UK worker | Direct HTTP or browser execution against target websites |
| Target translation | Maps owner cases to one target and converts its response to the common result |

---

## 07 | The controlled worker

### What it is

A controlled worker is a **dedicated, managed computer in the target country that executes the quote journeys**. It can be:

- a virtual machine in the owner's existing UK infrastructure;
- a UK-region cloud virtual machine in Azure, AWS or another approved provider; or
- a dedicated physical Windows computer in a UK office.

It is not a special commercial product. The owner does not have to buy Azure or AWS if suitable infrastructure already exists.

“Controlled” means:

- the machine is dedicated to this workload or strongly isolated;
- the owner knows where it runs and who can access it;
- software and browser versions are managed;
- credentials and test data are protected;
- it has a known UK network location;
- jobs, results and failures are recorded;
- it can be patched, stopped and rebuilt; and
- it does not expose a public inbound service merely to receive work.

The controlled worker improves security, repeatability and supportability. It does **not** guarantee that a target will accept a cloud IP address.

### Why not run on ordinary employee PCs?

Copying the application to many employee PCs would create inconsistent software versions, uncontrolled local data, weak auditability and a larger support surface. Variable IP addresses are not a sound production design.

A temporary supervised test on a willing person's UK household connection may be possible, but it should be a separately approved diagnostic test, using artificial data and a disposable managed machine or isolated account. It should not become the normal operating model.

### Recommended starting worker

For the pilot, use one scheduled UK virtual machine:

- 2-4 virtual CPU cores;
- 8-16 GB memory;
- 128 GB managed disk;
- fixed UK region and stable outbound IP;
- current managed Windows image;
- no direct public inbound port;
- owner-approved remote support route; and
- start/deallocate schedule so compute is paid only when required.

The pilot measures actual journey duration and safe concurrency. That evidence determines the final worker size and weekly running hours.

The preferred ownership is the owner's existing approved cloud subscription. If cloud onboarding would delay the pilot, a supplier-managed temporary UK worker can be used by explicit agreement and then removed or migrated after the review. The operational worker should sit under owner control.

### Owner cost and effort

Python and Playwright have no runtime licence charge. The owner pays for the machine, Windows entitlement where applicable, storage, network, monitoring and its own IT operation.

An Azure UK South worker provides a useful conservative planning example. The following ranges include the virtual machine, normal storage, a stable address and light monitoring:

| Operating model | Estimated external service cost |
|---|---:|
| Scheduled 2 vCPU worker | **£550-£900/year** |
| Scheduled 4 vCPU worker | **£850-£1,350/year** |
| Always-on 2 vCPU worker | **£1,550-£1,800/year** |
| Always-on 4 vCPU worker | **£2,800-£3,000/year** |
| Temporary 10-day pilot worker | **approximately £75-£150** |

Figures are indicative retail estimates as at 27 July 2026. They exclude VAT, corporate discounts, premium support and owner-specific security products, and are not an Azure quotation.

The recommended owner planning allowance is **£1,500 per year for one scheduled 4 vCPU UK worker**, subject to pilot runtime. This deliberately leaves some headroom.

Owner IT effort is likely to be:

| Owner situation | Indicative owner IT effort |
|---|---:|
| Existing approved cloud subscription and standard VM pattern | **2-5 MD one-off** |
| New cloud provider, security review and commercial onboarding | **5-10 MD one-off**, with potentially longer lead time |
| Ongoing patching, access and cost review | **0.25-0.5 MD/month** |

A Windows 11 desktop in Azure may require an eligible Microsoft 365, Windows Enterprise or VDA entitlement. A headless Windows Server worker uses the cloud provider's Windows Server pricing model. The owner's IT/licensing team should select and confirm the compliant image. Azure Virtual Desktop is optional; it is useful when staff need a managed interactive desktop but is not required merely to run a scheduled worker.

### Practical weekly operation

The stand-alone flow is intentionally simple:

1. an authorised user exports or places the approved test-case file in a protected job folder;
2. the worker is started automatically;
3. it reads a versioned copy of the cases;
4. it runs the selected target journeys;
5. it writes a result file and diagnostics;
6. the result is returned to a protected results folder; and
7. an authorised user reviews or downloads it.

Windows Task Scheduler is sufficient for an early stand-alone version. A later Peril Manager v-11 integration can replace the folders with controlled imports, job status, persisted results, reporting and audit.

---

## 08 | Chances, limitations and decision rules

### A reasonable route through increasing difficulty

| Level | Owner-facing description | Typical use |
|---|---|---|
| **L1 - Direct request** | Send the required information directly, similar to the supplied German sample | Fast and efficient where an appropriate stable request route exists |
| **L2 - Browser journey** | Use a real browser to complete the public quote journey | Used where the website expects browser behaviour and session state |
| **L3 - Operational browser journey** | Add reliable navigation, pacing, session isolation, restart and diagnostics | Needed for repeatable weekly operation |
| **L4 - Supervised repair** | Detect a changed result or journey and help a developer locate and repair it | Used after target changes; not autonomous access-control bypass |

The supplier starts with the simplest method that is both technically suitable and approved. L1 is time-boxed. If it is not promising, effort moves to L2 or to a better target rather than repeatedly forcing the same route.

### Main risks

| Risk | Consequence | Decision rule |
|---|---|---|
| Target terms or owner policy do not permit the activity | Work cannot proceed on that target | Obtain owner legal/compliance approval before recurring use |
| Target blocks cloud or automated access | No quote or intermittent completion | Test another approved UK network or replace the target |
| Target journey changes | Existing translation fails | Repair within a bounded estimate or replace target |
| Result is plausible but wrong | Business decision could be misleading | Use manual reference checks and visible exceptions |
| Products are not comparable | Price ranking may be invalid | Move from S1 to S2 fields where needed |
| Portal panel changes | Market coverage changes | Record returned insurer/product and review target value |
| Too much concurrency triggers restrictions | Runs become unreliable | Use measured pacing and worker capacity from the pilot |

### Stop conditions

Stopping is a successful pilot outcome when:

- the selected target cannot produce reliable and permitted results;
- price without additional product detail is not useful;
- recurring effort is disproportionate to the information gained;
- owner IT cannot provide an acceptable operating environment; or
- legal/compliance review does not approve the intended activity.

The owner should not continue merely because development has already started.

---

# Technical Background

## 09 | Architecture for IT review

### Recommended separation

Peril Manager v-11 can be the control and reporting layer, but it should not need to execute browser journeys on the existing IIS/database sandbox server.

```text
Owner test cases
       |
       v
Peril Manager v-11 or protected job storage
  - import/export
  - access and audit
  - job and result records
       |
       | outbound/polled job package
       v
Controlled UK worker
  - Python runtime
  - direct HTTP or Playwright
  - target-specific translations
  - local temporary workspace
       |
       | HTTPS
       v
Portal / insurer public quote journeys
       |
       v
Normalized results and diagnostics
       |
       v
Peril Manager v-11 or protected result storage
  - view/filter/report
  - export
  - history
```

The worker can poll for approved jobs and upload results over outbound HTTPS. No inbound Internet listener is required on the worker.

### Why the current Peril Manager v-11 sandbox is not the preferred worker

The current server hosts the sandbox database and Peril Manager v-11 applications through IIS. Adding browser execution there would:

- mix an external automation workload with database and application hosting;
- compete for CPU and memory;
- install browsers and an additional runtime on a shared server;
- make patching and incident isolation harder;
- expose all runs through the same sandbox IP; and
- increase the consequence of a browser/runtime defect.

For a small developer-only experiment it may be technically possible, but it is not the recommended pilot or operational architecture.

## 10 | Access methods

### Direct HTTP

The supplied German sample is a Python HTTP client. It constructs HTTPS requests, supplies headers and data, receives responses and parses them. It does not run a browser.

Benefits:

- small runtime footprint;
- high throughput;
- simple deployment; and
- easier structured response handling.

Limitations:

- a private web endpoint can change without notice;
- browser-created cookies, tokens and state may be required;
- headers alone do not reproduce a full browser session;
- the target may distinguish data-centre or automated traffic; and
- technical feasibility does not by itself establish permitted use.

### Browser automation with Playwright

Playwright starts and controls a real browser engine. It navigates pages, enters fields, clicks controls, waits for browser events and reads page or network results. The browser generates normal protocol behaviour, cookies, storage and script execution that a simple HTTP client does not provide.

Playwright is therefore not “between an API and a browser”; it **is browser control**. It still remains observable as automation and should not be presented as indistinguishable from a person.

Normal operational measures include:

- waiting for page and network state rather than fixed delays;
- using separate browser contexts for cases;
- preserving only the session state that the journey requires;
- controlled request pacing and concurrency;
- deterministic input and output;
- screenshots or traces for selected failures; and
- explicit handling of changes, referral and challenges.

Intentional typing mistakes, deceptive identity changes and CAPTCHA bypass are not part of the design.

## 11 | Network and location

The receiver normally sees the public IP address of the worker's Internet connection, not the user's local PC and not the Peril Manager v-11 server when the worker is separate.

It may also observe:

- HTTP headers;
- cookies and browser storage;
- TLS and connection characteristics;
- navigation and request sequence;
- JavaScript/browser capabilities;
- timing, concurrency and repetition;
- account or session identifiers;
- submitted quote data; and
- history associated with the public IP or session.

A UK cloud region gives a UK data-centre IP, not a household IP. This is good for controlled geography and operations but may be treated differently by a target. A UK office or household connection can provide a consumer/office network profile, but it creates operational and support concerns and must not be used as an undisclosed evasion technique.

IT should decide whether a second approved worker/network is justified only after the first pilot shows a location-dependent issue.

## 12 | Security and operations

Minimum IT controls for the controlled worker:

- dedicated resource group/project and tagged cost owner;
- current supported Windows image and patch policy;
- endpoint protection required by owner policy;
- named administrators with multi-factor authentication;
- no public RDP port; use the owner's approved private or managed access route;
- non-interactive worker identity with least privilege;
- encrypted OS disk and protected job/result storage;
- owner-defined data retention;
- secrets held outside source code;
- outbound target restrictions where practical;
- case/run identifiers without unnecessary personal data;
- central job, status and failure logs;
- defined browser/runtime update process;
- start/deallocate schedule and cost alert; and
- rebuild and rollback instructions.

The test cases should contain no real customer data. Any realistic addresses, email addresses or telephone numbers used to satisfy a form require owner approval and a retention rule.

## 13 | IT review questions

The owner's IT department is asked to review and comment on:

1. Is there an existing UK Azure/AWS subscription or approved virtualization platform?
2. Is Windows Server acceptable for a non-interactive worker, or is Windows 11/AVD required?
3. Which eligible Windows and remote-access licences already exist?
4. Can the worker be deallocated outside scheduled runs?
5. Which private administration route is required?
6. Where should job files, results, traces and logs be stored?
7. What retention and deletion periods apply?
8. Which endpoint protection and monitoring agents are mandatory?
9. Are outbound connections restricted or allow-listed?
10. Can a stable public outbound IP be assigned?
11. Who owns patching, cost alerts and incident response?
12. Is a temporary supplier-managed UK worker acceptable for the pilot, or must the owner host from day one?

---

## 14 | Decisions required before Round 1

### Business owner

- approve the first UK target;
- provide the approximately 250 artificial test cases;
- confirm S1 as the minimum result or select S2;
- decide whether all portal offers or only selected offers are required;
- identify the person who will judge product comparability; and
- approve the 10 MD pilot and review gate.

### Legal/compliance

- approve the intended recurring quote activity and test data;
- review relevant target terms and permitted use;
- confirm that no policy will be purchased or bound;
- approve network/location assumptions; and
- define evidence and retention expectations.

### IT

- select or approve the controlled UK worker;
- confirm licensing and access;
- provide secure input/result storage;
- apply owner security controls; and
- agree the operational owner and support route.

### Supplier

- deliver the time-boxed pilot;
- expose failures and limits honestly;
- avoid access-control bypass;
- produce actual result evidence;
- retain reusable code and artifacts; and
- propose the next 10 MD round only when justified.

---

## 15 | Sources and pricing basis

Market sources, accessed 25-27 July 2026:

1. Association of British Insurers, [2024 property premium and policy tracker](https://www.abi.org.uk/news/news-articles/2025/2/more-action-needed-to-protect-properties-as-adverse-weather-takes-record-toll-on-insurance-claims-in-2024/).
2. MoneySuperMarket, [Home insurance](https://www.moneysupermarket.com/home-insurance/).
3. Go.Compare, [Home risk report](https://www.gocompare.com/home-insurance/home-risk-report/).
4. Confused.com, [Home insurance providers](https://www.confused.com/home-insurance/providers).
5. Compare the Market, [Home insurance](https://www.comparethemarket.com/home-insurance/).
6. Insurance Ireland, [Factfile 2024](https://insuranceireland.eu/wp-content/uploads/2026/01/Insurance-Ireland-Factfile-2024.pdf).
7. Central Statistics Office, [Census 2022 - Housing in Ireland](https://www.cso.ie/en/releasesandpublications/ep/p-cpp2/censusofpopulation2022profile2-housinginireland/keyfindings/).
8. bonkers.ie, [Compare home insurance](https://www.bonkers.ie/compare-home-insurance/).
9. Chill, [Panel of insurers](https://www.chill.ie/insurers/).
10. Compare Insurance Ireland, [House insurance](https://www.compareinsuranceireland.ie/house-insurance/).

Technical and cost sources:

11. Microsoft, [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices).
12. Microsoft, [Windows Virtual Machines pricing](https://azure.microsoft.com/en-gb/pricing/details/virtual-machines/windows/).
13. Microsoft, [Azure Virtual Desktop licensing](https://learn.microsoft.com/en-us/azure/virtual-desktop/licensing).
14. Microsoft, [Understand and estimate Azure Virtual Desktop costs](https://learn.microsoft.com/en-sg/azure/virtual-desktop/understand-estimate-costs).
15. Microsoft, [Deploy Windows 11 on Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/windows-desktop-multitenant-hosting-deployment).
16. Playwright, [Browsers](https://playwright.dev/docs/browsers).
17. Playwright, [Network](https://playwright.dev/docs/network).

The worker figures are rounded planning allowances. Actual owner prices depend on contract, discounts, reservation, running schedule, worker size, security services and tax. The owner's cloud calculator or supplier quotation remains authoritative.

---

## Closing recommendation

Commission the 10 MD UK pilot, provision one controlled UK worker and adopt S1 - price plus insurer/product name - as the provisional minimum result. Confirm the five result questions in Section 03 before development begins.

Review actual evidence at the end of the pilot. Continue with one further 10 MD round only when the owner can state what additional result or operational improvement it is buying.
