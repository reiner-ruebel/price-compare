# Household Insurance Price Comparison

## Delivery and Effort Matrix

**Prepared for:** ERGO UK and Ireland  
**Estimate date:** 25 July 2026  
**Estimate unit:** one person-day (MD) = eight working hours  
**Status:** ROM estimate for scope and budget approval; re-baseline after the technical spike

## Executive recommendation

Build the first operational pilot in **Python with Playwright**, run it from a controlled **UK-based execution host**, and cover:

- one major UK comparison portal;
- three direct UK insurer quote journeys;
- CSV input and output;
- raw evidence, audit history, validation and monitoring; and
- two structured user-acceptance and change cycles.

This is a market-intelligence system, not a sales channel. It will not itself create any of the target 25,000 policies.

The recommended minimum is **103–154 MD once** and **8–16 MD per month** for operation and maintenance. The market scan is included at no charge, although its effort is shown.

Do not promise that Playwright, an AI agent, rotating headers or a distributed desktop application will make the traffic invisible. They will not. A real browser improves compatibility with modern quote journeys, but automated behaviour, sessions and network patterns remain detectable. The service must therefore fail visibly, retain evidence and stop when results cannot be trusted.

## Scope assumptions

The estimate is based on the following:

1. The first country is the United Kingdom.
2. “1,000 inquiries per week” means **1,000 quote journeys in total across all target sources**, not 1,000 cases sent to every source.
3. If the same 1,000 cases are run against four sources, the actual load is 4,000 quote journeys per week. Capacity and target acceptance must then be re-tested.
4. A quote journey ends at a quote, decline or classified failure. It does not buy or bind a policy.
5. The owner provides approved quote personas, controlled contact details, a UK execution environment, and timely access to subject-matter experts.
6. No CAPTCHA-solving service, access-control bypass or attempt to defeat a technical restriction is included.
7. One connector means one public quote journey for one portal or insurer brand. A materially different product or journey is another connector.
8. Estimates assume normal public web forms. Account creation, MFA, persistent CAPTCHAs, contractual API onboarding or a major redesign are change controls.

## Minimum operational pilot

“Creation” is one-time delivery effort. “Maintenance” is expected effort per calendar month after launch. Monthly effort is capacity: the exact mix will move between monitoring, regression testing and break/fix work as target sites change.

| ID | Result | Classification | Creation (MD) | Maintenance (MD/month) | Commercial treatment | Relevant comment |
|---|---|---:|---:|---:|---|---|
| B1 | UK target and market map, source register and prioritised pilot shortlist | Baseline | 5–7 | 0.5–1.0 | **No fee** for creation | Comparison brands and underlying insurers must not be double-counted. |
| B2 | Canonical household-risk and quote schema, CSV contract and representative scenario pack | Baseline | 6–9 | 0.5 | Included | Buildings, contents and combined cover are separate products; flats and tenants need different treatment. |
| B3 | Technical spike proving one portal, one direct insurer and UK-hosted execution | Baseline | 6–10 | — | Included | This is the go/no-go gate and the point at which the estimate is re-baselined. |
| B4 | Python batch runner with CSV import/export, configuration, secrets, checkpoints and safe restart | Baseline | 12–18 | 0.5–1.0 | Included | New implementation; the supplied German script is a reference, not a production base. |
| B5 | One UK comparison-portal connector | Baseline | 15–22 | 1.5–3.0 | Included | A single portal can return many brands, but creates a concentrated dependency. |
| B6 | Three direct UK insurer connectors | Baseline | 18–27 | 1.5–3.0 | Included | Equivalent to 6–9 MD creation and 0.5–1.0 MD/month per standard connector. |
| B7 | Evidence and data-quality controls: raw response, screenshot, field lineage, semantic validation and anomaly alerts | Baseline | 8–12 | 1.0–2.0 | Included | Required because a technically successful response can still contain a wrong or misleading price. |
| B8 | Resilience and controlled throughput: rate limits, retry policy, circuit breaker, scheduling and monitoring | Baseline | 7–10 | 1.0–2.0 | Included | Repeated failure or suspicious variation stops a target; it does not trigger more aggressive traffic. |
| B9 | Security, privacy, access control and retention configuration | Baseline | 3–5 | 0.25–0.5 | Included | Use synthetic or owner-controlled personas; do not use customer data by default. |
| B10 | Automated testing, volume test, manual reconciliation, owner UAT and two change cycles | Baseline | 15–22 | 1.0–2.0 | Included | A one-week “test phase” is not a credible assumption for four independent external journeys. |
| B11 | UK deployment, operating runbook, user guide, training and production release | Baseline | 6–9 | 0.25–0.5 | Included | Development may occur in Spain or Germany; production quote execution should be in the target country. |
| B12 | Counsel-ready description of the technical activity and decision checklist | Baseline | 2–3 | — | Included | Describes the facts for the owner’s lawyers; it is not a legal opinion. |
|  | **Total** |  | **103–154** | **8–16** |  | Creation total includes 5–7 MD supplied at no fee. |

### Provisional acceptance measures

The spike will confirm final thresholds. The proposed measures are:

- the agreed weekly volume completes inside its operating window;
- every journey has a classified outcome: quote, legitimate no-quote/decline, blocked/challenged, target error or system error;
- at least 95% of technically eligible journeys have a classified outcome with evidence;
- there is no silent price substitution or silent reuse of a stale quote;
- sampled prices and material cover fields reconcile to the visible result;
- every run records target, scenario version, timestamp, execution region and software version; and
- the system suspends a connector when confidence falls below the agreed threshold.

No fixed quote-yield percentage can be promised before the target forms and scenario set are known. Insurers may legitimately decline risks.

## Optional scope

Optional rows are additive unless marked as an alternative. Packaged totals must not be added to their component rows.

| ID | Result | Classification | Creation (MD) | Maintenance (MD/month) | Relevant comment |
|---|---|---:|---:|---:|---|
| O1 | Each additional standard UK direct-insurer connector | Optional | 6–9 each | 0.5–1.0 each | Prioritise by observed portal presence and commercial relevance. |
| O2 | Each additional UK comparison-portal connector | Optional | 15–22 each | 1.5–3.0 each | The four major portal brands should not be assumed to produce independent insurer panels. |
| O3 | Complete the other three major UK comparison portals | Optional package | 45–66 | 4.5–9.0 | Package equivalent to three O2 connectors. |
| O4 | Ireland country enablement: Eircode/address rules, currency, product mapping and regional runner | Optional | 5–8 | 0.5–1.0 | UK and Republic of Ireland products and questions are not interchangeable. |
| O5 | Each standard Republic of Ireland direct-insurer connector | Optional | 6–10 each | 0.5–1.5 each | Candidate brands require owner confirmation after market and journey review. |
| O6 | Each Republic of Ireland comparison/broker portal connector | Optional | 14–22 each | 1.5–3.0 each | Irish services have narrower and differently structured panels than the large UK portals. |
| O7 | Ireland starter pack: country enablement, one portal and three direct insurers | Optional package | 37–60 | 3.5–8.5 | Includes O4, one O6 and three O5 connectors. |
| O8 | Implement the baseline platform in .NET instead of Python | Optional alternative | **+10–18** versus baseline | broadly unchanged | Choose this only if a single .NET deployment is more important than fastest delivery. Playwright is available for .NET. |
| O9 | Integrate the Python service into the existing Portal through its API, with audit, case management and reporting UI | Optional | 24–36 | 2–4 | Recommended later if multiple users, central audit and scheduled reporting become necessary. |
| O10 | Build a separate application on the Portal Foundation | Optional alternative to O9 | 35–50 | 3–5 | Cleaner separation, but duplicates deployment and product ownership. |
| O11 | Distribute a compiled Windows desktop application | Optional; not recommended | 18–28 | 2–4 | Multiple installations create version, evidence and support problems. Users in one office may still share one public IP. |
| O12 | AI-assisted change detection and supervised connector-repair proof of concept | Optional experiment | 10–16 | 2–4 | Use AI to propose repairs for review, not to make unsupervised production quote decisions. It does not hide automation. |
| O13 | Additional owner UAT/change cycle beyond the two baseline cycles | Optional | 3–6 per cycle | — | Covers changed requirements, retest and release, not a new connector. |
| O14 | Business dashboard for price position, coverage and historical trends | Optional | 10–16 | 1–2 | The baseline provides operational output and audit, not a management-information product. |
| O15 | Additional controlled country execution host | Optional | 3–5 | 0.5–1.0 | Cloud, network and licence charges are excluded. |

## Technology decision

| Choice | Decision | Reason |
|---|---|---|
| Python + Playwright | **Baseline** | Fastest fit with the current team and CSV workflow; handles browser-driven forms and still permits network-level evidence capture. |
| Python `requests` against private web endpoints | Do not use as the general design | It can be efficient for a stable documented API, but private quote endpoints and payloads change without notice. |
| .NET + Playwright | Viable alternative | Best when one-stack Portal operations outweigh the additional initial effort. It does not improve resistance to blocking. |
| Runtime AI agent | Not baseline | More nondeterministic, harder to validate and audit, and still automatable traffic. |
| Compiled desktop deployment | Not recommended | Weak central control and a poor substitute for an explicit regional execution design. |

## Commercial and business perspective

At the stated average premium, 25,000 policies represent **£10 million of annual written premium**. The stated 1,000 quote inquiries per week represent about **52,000 inquiries per year**.

Those numbers must not be read as a 48% sales conversion assumption. These are competitor-research inquiries, not prospective customers. The pricing tool may support product and pricing decisions, but acquisition, distribution, underwriting, service and claims capabilities determine policy sales.

The volume is technically modest. Reliability and representativeness matter more than raw count. A smaller, stable panel of well-designed scenarios is more useful than 52,000 untrusted quotes.

## Exclusions and estimate controls

The effort excludes:

- VAT, travel, cloud hosting, network, proxy, CAPTCHA, LLM and third-party licence charges;
- negotiation of API access, commercial data licences or target-site permission;
- legal advice or counsel fees;
- product pricing, actuarial modelling, customer acquisition or policy administration;
- purchase or binding of insurance;
- use of real customer data unless separately approved and designed;
- bypass of authentication, access controls, CAPTCHAs or other technical restrictions; and
- guaranteed uninterrupted access to third-party public websites.

The estimate remains valid for 30 days and is subject to the spike. A target redesign, new mandatory identity verification, persistent challenge, material question-set expansion or a change from 1,000 total journeys to 1,000 journeys per target will trigger re-estimation.

## Market context used for this estimate

- The Association of British Insurers reported an average 2024 combined buildings-and-contents premium of £395 and stated that its tracker analyses 16.5 million policies sold per year: [ABI, February 2025](https://www.abi.org.uk/news/news-articles/2025/2/more-action-needed-to-protect-properties-as-adverse-weather-takes-record-toll-on-insurance-claims-in-2024/).
- Current portal claims illustrate the breadth and maintenance exposure: MoneySuperMarket states 103 UK home-insurance providers, Go.Compare states 82 active home insurers, and Confused.com lists 83 insurance companies: [MoneySuperMarket](https://www.moneysupermarket.com/home-insurance/), [Go.Compare](https://www.gocompare.com/home-insurance/guide/how-to-choose-the-best-home-insurance/), [Confused.com](https://www.confused.com/home-insurance/providers).
- Insurance Ireland reported €657.5 million of household gross written premium for 2024: [Insurance Ireland Factfile 2024](https://insuranceireland.eu/wp-content/uploads/2026/01/Insurance-Ireland-Factfile-2024.pdf).
- Ireland’s portal market is narrower: bonkers.ie currently identifies Aviva and Zurich as its home-insurance partners, while Chill describes a broader intermediary panel across products: [bonkers.ie](https://www.bonkers.ie/compare-home-insurance/), [Chill](https://www.chill.ie/insurers/).

