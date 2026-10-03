# Household Insurance Price Comparison

## Internal Estimate Basis, Work Breakdown and Market Research

**Prepared for:** ERGO UK and Ireland  
**Date:** 25 July 2026  
**Purpose:** internal delivery planning and estimate substantiation  
**Related external document:** `price-comparison-effort-matrix-external.md`

## 1. Bottom line

Recommend a UK pilot built in Python with Playwright, operated on a controlled UK host, with one major comparison portal and three direct insurers.

- One-time delivery effort: **103–154 MD**
- Of that effort, market research is **5–7 MD at no charge**
- Expected maintenance capacity: **8–16 MD/month**
- Credible elapsed time with one developer: roughly **5–8 calendar months**, allowing for owner decisions and UAT
- Credible elapsed time with two effective delivery staff: roughly **3–5 calendar months**; external dependencies prevent perfect parallelisation

The maintenance estimate is deliberately not small. Four independent third-party quote journeys, browser versions, address services, product questions and result layouts will change without notice. A proposal showing only a few maintenance hours per month would be optimistic.

The pilot should not be represented as capable of driving 25,000 sales. It is a pricing-intelligence tool.

## 2. Corrections to the initial concept

### 2.1 Household insurance is not one uniform product

The supplied description is too broad:

- UK and Irish home insurance commonly separates buildings, contents and combined cover.
- A freeholder normally insures the building; a tenant generally needs contents cover only.
- A flat owner may have building cover through a freeholder, management company or block policy and therefore buy contents cover only.
- Rebuild cost, not property market value, is normally the relevant buildings sum insured.
- Owner-occupier, landlord, tenant, holiday-home, unoccupied and non-standard risks are different journeys.

The initial scenario pack must therefore state exactly which risk and cover combinations ERGO wants to benchmark. Comparing a contents-only result with a combined result would produce a neat but false price comparison.

### 2.2 Quote volume does not imply sales conversion

The commercial target is:

- 25,000 policies;
- at an asserted average premium of £400;
- therefore £10 million annual written premium.

The collection target is approximately 52,000 inquiries per year. These inquiries are synthetic market observations, not customer leads. Dividing 25,000 policies by 52,000 observations produces 48.1%, but that is not a conversion rate and must not appear in a business case.

The ABI says its UK property tracker analyses 16.5 million policies sold per year. A 25,000-policy target is about 0.15% of that tracked count, but this is only a scale illustration: the definitions and periods are not identical.

For pricing intelligence, statistical coverage of locations and risks matters more than repeating similar cases. The product team should own a sampling design covering region, property type, age, rebuild value, occupancy, claims, security, excess and cover selection.

### 2.3 “1,000 inquiries” is ambiguous

There are two materially different loads:

- **1,000 total case-target journeys per week**, divided among sources; or
- **1,000 cases per week sent to every target**.

With one portal and three insurers, the second interpretation is 4,000 browser journeys per week. The external estimate assumes the first interpretation. The spike must measure the average end-to-end journey time and define the safe concurrency for each target.

### 2.4 Browser automation does not hide crawling

Playwright should be used because it drives current browser engines and handles JavaScript forms, session state and network evidence. It is not a concealment product.

Modern bot systems use headers, session characteristics, browser signals, JavaScript detection, fingerprints and behavioural models. Rotating a user-agent string or launching a headed browser does not change that fact. An AI agent uses the same observable browser and network path and adds nondeterminism.

The defensible technical posture is:

- controlled rate and concurrency;
- stable, declared operating configuration;
- owner-approved personas;
- evidence for every outcome;
- anomaly detection;
- circuit breakers and operator review; and
- no attempt to bypass a challenge or technical restriction.

### 2.5 Geographic execution matters

Development in Spain and Germany is acceptable. Production-like tests from those locations are not representative of UK consumer access and may affect:

- geolocation and eligibility;
- content and consent variants;
- currency or address lookup;
- latency;
- fraud and bot scoring; and
- quoted price or quote availability.

Use an owner-controlled UK host for UK runs and an Irish host for Republic of Ireland runs. A fixed country host is not guaranteed to avoid blocking; it makes geography, evidence and operations consistent.

### 2.6 Multiple desktop users are not an IP strategy

A compiled Windows application is a poor way to obtain IP diversity:

- staff in one office may share a single public NAT address;
- home networks and machines are inconsistent;
- results become harder to reproduce;
- secrets and evidence spread across endpoints;
- upgrades and emergency shutdowns are slower; and
- support effort rises.

Build a centrally controlled service first. Add regional execution nodes only for a defined operational reason.

## 3. Assessment of the supplied German assets

Files reviewed in `origs`:

- `huk_crawler.py`
- `utils.py`
- `standard_input(in).csv`

No result file was present, despite the prompt referring to one. The script also expects `standard_input.csv`, while the supplied file is named `standard_input(in).csv`, so the supplied package does not run as-is without adjustment and environment-specific credentials.

### Useful ideas to retain

- tabular scenario input;
- a translation layer from input fields to target fields;
- raw response retention;
- joining quote output back to the input row;
- controlled delay between requests; and
- potential parallel work allocation.

### Reasons not to use it as the production base

| Finding | Consequence |
|---|---|
| It supports one German HUK journey and hard-codes private endpoints, including an endpoint version. | It is not a multi-target, UK/Irish connector architecture. |
| It uses direct `requests` calls rather than the public browser journey. | Private payloads can change without notice and browser/session controls are missed. |
| Proxy credentials are assembled from a plaintext password file in a user’s Documents folder during import. | Poor portability and secret management. |
| A random user-agent and random 2–4 second sleep are intended to “not stand out.” | These do not prevent automated-traffic classification. |
| Error handling mainly catches non-JSON responses. There is no retry taxonomy, backoff, circuit breaker or semantic validation. | Blocked, stale or intentionally wrong responses can be mistaken for data. |
| The address helper tries random initial letters until it finds a real street. | Results are difficult to reproduce and the data-use model is unclear. |
| The input is CSV, but final output is JSON and XLSX. | It does not meet the stated CSV workflow without work. |
| There are no automated tests, fixtures, versioned schemas or release controls. | Change risk and regression cost are high. |
| There is no durable run ledger or alerting. | Audit, operations and incident reconstruction are incomplete. |
| The parallel executor structure is present, but the main program recommends a single process and no safe target-specific concurrency model exists. | Throughput must be measured and controlled, not inferred. |

**Internal conclusion:** reuse the field-mapping lessons, not the codebase. Starting with a clean connector architecture is lower risk than progressively turning a single-target script into an auditable service.

## 4. Market research

### 4.1 United Kingdom scale

The ABI reported:

- an average combined buildings-and-contents premium of **£395 in 2024**; and
- a property tracker analysing **16.5 million policies sold per year**.

The large UK comparison portals expose broad and overlapping panels:

| Portal | Current public evidence | Internal implication |
|---|---|---|
| MoneySuperMarket | States that it compares 103 UK home-insurance providers. | Broad panel; brand variants must not be counted as independent underwriters. |
| Go.Compare | States 82 active home insurers on its panel as at 1 July 2026. | Broad panel and publicly described feature comparison. |
| Confused.com | Lists 83 home-insurance companies as at April 2026. | Transparent public provider list is useful for target mapping. |
| Compare the Market | Major national portal with a current household quote journey. | Treat as Tier 1 even though the reviewed page did not state a directly comparable current panel count. |

The four should be treated as the initial comparison-portal universe. Do not claim a current market-share ranking without licensed or verified current data.

Candidate direct targets appearing in current portal panels include:

- Admiral;
- Allianz;
- Aviva;
- AXA;
- Churchill;
- Hastings;
- LV=;
- Policy Expert;
- Tesco Insurance; and
- relevant specialist/digital brands.

This is a target pool, not the recommended final three. Select direct targets after:

1. grouping brands by insurer/underwriter and quote technology;
2. observing which brands repeatedly appear for ERGO’s scenario set;
3. checking whether the direct journey is materially different from the portal result;
4. confirming product comparability; and
5. completing the technical feasibility spike.

Suggested pilot portal selection method:

- allocate no more than two spike days to each of two Tier 1 candidates;
- score journey stability, result richness, evidence capture, challenge frequency and product comparability;
- choose one for the baseline;
- retain the second as the first optional portal and an independent cross-check.

### 4.2 Republic of Ireland scale

Insurance Ireland’s 2024 Factfile reports:

- **€657.5 million** household gross written premium;
- €425.1 million net earned premium; and
- €263.9 million net claims incurred.

The 2022 Census counted **1.86 million occupied households**. This gives useful market scale, but it does not provide a current count of household insurance policies.

The Irish comparison market is materially narrower and differently structured:

| Service | Current public evidence | Internal implication |
|---|---|---|
| bonkers.ie | Says home policies are available from Aviva and Zurich. | Useful portal, but not a broad whole-market panel. |
| Chill | Describes a panel of 14 insurers across its product offering and identifies home-capable insurers/underwriters. | Broker/intermediary flow; the home subset and quote-return mechanics require a spike. |
| Compare Insurance Ireland | Names examples including Aviva, Zurich, AXA, Allianz and AIG, subject to eligibility. | Confirm whether the journey returns comparable online prices or broker follow-up. |

Candidate Irish direct targets:

- Allianz;
- Aviva;
- AXA;
- FBD;
- Zurich;
- 123.ie / Intact-RSA-related propositions;
- AIG where a consumer home journey is available; and
- broker-distributed products only where ERGO expressly wants them.

Insurance Ireland’s non-life member directory is broader than consumer home insurance. Membership alone must not be used as evidence that a firm offers a public household quote journey.

### 4.3 Research conclusion

Start in the UK. It offers greater portal breadth and provides a better test of a comparison-led intelligence approach.

For Ireland, do not copy the UK design blindly. A sensible starter pack is one portal/broker journey plus three direct insurers. Because portal coverage is narrower, direct connectors contribute more incremental market visibility.

## 5. Baseline work breakdown

The table reconciles exactly to the external baseline. Each range includes implementation, tests, expected initial defect fixing and documentation where relevant.

| ID | Work behind the result | Creation effort |
|---|---|---:|
| B1 | Market discovery 3–4; brand/underwriter grouping 1; prioritisation and source register 1–2 | **5–7** |
| B2 | Product/question taxonomy 2–3; canonical schema and CSV contract 2–3; representative scenario design 2–3 | **6–9** |
| B3 | Target reconnaissance 2–4; browser-flow proof 2–3; regional access and throughput proof 1–2; spike record and re-estimate 1 | **6–10** |
| B4 | Batch orchestration 3–4; CSV input/output 2–3; checkpoints/idempotency 2–3; configuration/secrets 2–3; unit tests 2–3; developer documentation 1–2 | **12–18** |
| B5 | Portal form and result mapping 3–4; connector implementation 5–7; result/evidence extraction 2–3; session handling 1–2; fixtures and tests 3–4; initial defect fixing 1–2 | **15–22** |
| B6 | Per direct connector: investigation 1–2; implementation 2–3; validation 1–2; tests 1; initial defect fixing 1; repeated for three targets | **18–27** |
| B7 | Evidence store 2–3; schema and completeness validation 2–3; anomaly rules 2–3; manual reconciliation tooling 1–2; tests 1 | **8–12** |
| B8 | Target rate/concurrency controls 2–3; retry taxonomy and circuit breaker 2–3; scheduling/checkpoints 1–2; monitoring 1; failure tests 1 | **7–10** |
| B9 | Data inventory and retention 1; secret and role design 1; privacy/DPIA inputs 1–2; security verification 0–1 | **3–5** |
| B10 | Test environment/data 2–3; integration/regression tests 4–6; volume/soak test 2–3; owner UAT 2–3; two feedback cycles 4–6; release defect closure 1 | **15–22** |
| B11 | UK deployment 2–3; operating runbook 1–2; user guide 1; knowledge transfer 1; production release 1–2 | **6–9** |
| B12 | Factual technical-processing description 1–2; legal decision and evidence checklist 1 | **2–3** |
|  | **Total** | **103–154 MD** |

### What the test effort must cover

Development “works on my machine” testing is insufficient. The baseline test plan includes:

- field-by-field mapping against the visible form;
- valid quote, insurer decline, validation error, target outage, timeout, rate limit, challenge and changed-page cases;
- repeat runs of a stable sentinel panel to detect unexplained price or result-count variation;
- screenshot and network/result reconciliation;
- restart after partial batch failure without duplicate or stale results;
- CSV schema/version compatibility;
- UK postcode/address variants;
- concurrency and weekly-volume soak tests from the UK host;
- browser-version upgrade regression;
- permission, secret and retention checks;
- manual owner review of material cover fields, not price alone; and
- two formal UAT/feedback cycles.

Additional product or reporting requests after those two cycles use optional row O13.

## 6. Recurring maintenance basis

| Maintenance activity | Expected MD/month | Notes |
|---|---:|---|
| Source and product monitoring | 0.5–1.0 | Provider/panel and question changes |
| Scenario/schema stewardship | 0.5 | Controlled input changes |
| Core runtime and dependency maintenance | 0.5–1.0 | Python, Playwright and browser updates |
| Comparison-portal connector | 1.5–3.0 | Monitoring, repair and retest |
| Three direct connectors | 1.5–3.0 | 0.5–1.0 each |
| Evidence and data-quality review | 1.0–2.0 | Includes anomaly investigation |
| Runtime operations and incident response | 1.0–2.0 | Scheduling, failures and capacity |
| Security/privacy/retention review | 0.25–0.5 | Access and deletion verification |
| Release regression | 1.0–2.0 | Sentinel and changed connector tests |
| Runbook/user-document updates | 0.25–0.5 | Keep operations reproducible |
| **Total capacity** | **8–16** | Actual monthly mix varies |

Monthly capacity does not include new targets, product expansion, major target redesign, owner-requested feature development or infrastructure fees.

## 7. Proposed solution architecture

### 7.1 Baseline components

1. **Scenario registry**  
   Versioned CSV contract and validated canonical model.

2. **Orchestrator**  
   Creates case-target jobs, applies country/target limits, checkpoints progress and supports safe restart.

3. **Playwright connectors**  
   One isolated connector per quote journey. Page interactions use stable semantic locators where possible.

4. **Result normaliser**  
   Preserves the raw target result and creates comparable fields for price, taxes/fees, excess, cover limits, add-ons, insurer/brand and outcome.

5. **Evidence store**  
   Request/run metadata, visible result screenshot, relevant network payload where appropriate, target/result timestamp, scenario and connector versions, and hashes.

6. **Quality gate**  
   Completeness, range, consistency, stale-result and unexplained-variation checks. Failed confidence prevents publication.

7. **Operational output**  
   CSV for users, plus raw structured evidence for investigation.

8. **Monitoring and circuit breaker**  
   Alerts on result-count shift, price anomalies, target errors and challenge rates; suspends untrusted sources.

### 7.2 Portal integration

The recommended sequence is:

1. prove the quote service as a small, independently deployable Python service;
2. expose its existing/external API;
3. integrate the Portal only after the output and operating model are stable.

Portal integration should add:

- authenticated job submission;
- case and batch status;
- input upload/download;
- immutable audit references;
- exception review;
- scheduled reports;
- access roles; and
- data-retention controls.

Do not move browser-connector code into the Portal merely to make the stack uniform. A thin service boundary keeps volatile target logic isolated.

### 7.3 Python versus .NET

| Area | Python baseline | .NET alternative |
|---|---|---|
| Team fit and speed | Better | Acceptable |
| Existing German concepts | Easier to reference | Must translate |
| Playwright support | Strong | Strong |
| Portal deployment consistency | Requires service boundary | Better |
| CSV/data tooling | Strong | Adequate |
| Bot visibility | No advantage | No advantage |
| Auditability | Equivalent if designed correctly | Equivalent if designed correctly |

If immediate Portal-native deployment is a hard requirement, choose .NET once and do not first build a throwaway Python version. Otherwise, use Python and integrate through the Portal API.

### 7.4 Appropriate use of AI

AI can help during development and maintenance:

- summarise a changed page;
- propose locator or mapping updates;
- generate candidate test cases; and
- classify screenshots for operator review.

It should not initially:

- autonomously invent answers to insurance questions;
- accept terms or declarations;
- decide that an anomalous price is valid;
- work around a challenge; or
- change production connectors without review and regression testing.

This keeps quote generation reproducible and auditable.

## 8. Data-quality and wrong-quote controls

The German experience reports both blocking and plausible but wrong prices. HTTP status monitoring alone cannot detect the second failure mode.

Required controls:

- retain raw and normalised values;
- store the visible price and material coverage fields;
- bind every result to a scenario hash and session/run identifier;
- reject a result if scenario, currency, cover type, billing frequency or quote date do not match;
- use a small sentinel panel with expected structural behaviour;
- repeat a risk sample and alert on unexplained variance;
- compare portal and direct results where the products are genuinely equivalent;
- track number of returned brands/products and no-quote reasons;
- flag identical results across implausibly different risks;
- flag stale quote/reference reuse;
- sample manual reconciliation each release and each month; and
- suspend rather than publish when confidence is insufficient.

A price difference is not automatically an error. Channel discounts, product variants, panel timing and different answers can all create legitimate differences. The audit must preserve enough fields to explain them.

## 9. Key delivery risks

| Risk | Likelihood | Impact | Treatment |
|---|---|---|---|
| Target changes form or result contract | High | High | Connector isolation, fixtures, sentinel runs, maintenance capacity |
| Bot challenge or IP block | Medium–high | High | UK host, controlled rate, circuit breaker, evidence, owner decision; no bypass |
| Plausible but wrong quote | Medium | High | Semantic validation, repeat samples, direct/portal reconciliation, manual QA |
| Incomparable products | High without taxonomy | High | Canonical product model and material-cover capture |
| Requirements expand during UAT | High | Medium–high | Two baseline cycles, decision log, optional cycles thereafter |
| Portal integration is started too early | Medium | Medium | Stabilise standalone service contract first |
| Use of personal or uncontrolled contact data | Medium | High | Synthetic/controlled personas, minimisation, access and retention controls |
| Country location changes results | Medium | Medium–high | Country-specific runner and recorded execution region |
| Portal panel is mistaken for whole market | High | Medium | Source register, brand/underwriter grouping, direct-source sampling |
| Maintenance is underfunded | High | High | 8–16 MD/month planned capacity and connector-level ownership |

## 10. Counsel-ready technical activity description

### 10.1 Status and purpose

This section is a factual system and processing description prepared for legal review. It is not legal advice and does not state that any particular target, data field or operating method is permitted.

**Proposed activity:** ERGO UK and Ireland, or a contracted operator acting on its documented instructions, will submit pre-approved hypothetical household-insurance risk scenarios to publicly accessible online quote journeys operated by selected insurers and insurance comparison/intermediary services. The purpose is internal market, product and pricing analysis.

The system will collect displayed quote outcomes and material product attributes. It will not purchase, bind, renew, cancel or recommend a policy; represent that a genuine consumer intends to transact; or communicate the collected output to an end customer as personal advice.

### 10.2 Operating scope

- Initial territory: United Kingdom.
- Optional territory: Republic of Ireland.
- Initial volume assumption: up to 1,000 case-target quote journeys per week in total.
- Sources: one selected UK comparison portal and three selected direct insurer journeys.
- Access method: deterministic browser automation using Playwright from an owner-controlled UK execution host.
- Schedule: controlled batches within an approved operating window and target-specific concurrency.
- Stop conditions: challenge/access restriction, abnormal error rate, suspected wrong/stale results, unexplained material response change, owner instruction or legal/compliance hold.
- Prohibited technical behaviour: bypassing authentication or access controls, solving or outsourcing CAPTCHAs, exploiting a vulnerability, or escalating traffic after a restriction.

### 10.3 Data submitted

Only fields required for the approved quote scenarios will be submitted. Depending on the target, those fields may include:

- address or postcode/Eircode;
- property type, construction, age, rooms, roof and occupancy;
- rebuild cost and contents value;
- security, claims and cover selections;
- hypothetical policyholder age, occupation and household information; and
- owner-controlled email address or telephone number where technically mandatory.

The default design will not use existing customer or employee information. Personas and contact points will be generated or controlled by the owner, documented, used consistently where accuracy is required, and segregated from real consumer records. If a target requires information that cannot appropriately be supplied under the approved model, that target will be suspended pending owner and counsel review.

### 10.4 Data collected

The system may retain:

- quote price, taxes/fees and payment frequency;
- insurer, intermediary, brand and underwriter where disclosed;
- quote/reference identifier;
- cover type, excess, limits, inclusions, exclusions and optional covers displayed;
- quote, decline, validation and failure status;
- timestamps, target URL, execution country, connector and scenario versions;
- screenshots and relevant structured browser/network responses;
- cookies/session identifiers needed for the single quote journey; and
- technical logs such as response status, duration and challenge indicator.

No purchase, payment-card, claims-file or special-category data is intended.

### 10.5 Storage and access

- Normalised output will be made available as CSV.
- Raw evidence will be stored separately under role-based access.
- Secrets and controlled persona contact details will not be embedded in source code or CSV exports.
- Retention periods will be approved by the owner before production and implemented by data class.
- Evidence required for audit or dispute review will be integrity-protected and linked to the run record.
- UK and Irish data locations, processors and any cross-border access will be recorded before production.

### 10.6 Decisions required from owner’s counsel and compliance

Counsel should make and record a target-specific decision on:

1. the operator’s authority and the relevance of each target’s contractual terms and published access conditions;
2. whether the proposed frequency, automated submission and retention are within the approved activity;
3. the status and wording of answers, declarations, consents and statements presented by the target;
4. whether a dedicated owner identity must be disclosed or agreed with a target;
5. the treatment of a target challenge, block, cease request or technical restriction;
6. whether addresses, contact details, cookies, device identifiers or quote references are personal data in the implemented circumstances;
7. controller/processor roles, lawful basis, transparency, minimisation, accuracy and retention;
8. whether a UK or EU data protection impact assessment is required or prudent;
9. processors, hosting regions, access from Spain/Germany and international-transfer controls;
10. whether the activity could be understood as regulated insurance distribution, advice, arranging or customer-facing financial promotion, and the controls that keep it within internal research;
11. competition-law and confidential-information boundaries for use and circulation of the output;
12. record preservation, incident, complaint, data-subject and external-notice handling; and
13. the production approval, review interval and accountable owner.

### 10.7 Required approval record

Production should start only when the owner has approved:

- target register and permitted journey;
- approved scenario/persona set;
- approved fields and declarations;
- volume and schedule;
- country host and authorised operators;
- evidence and retention schedule;
- response to challenge/block/notice;
- data-protection and transfer record;
- legal/compliance decision owner; and
- periodic review date.

Any material change to target, country, submitted data, purpose, volume, access method or retention returns to review.

## 11. Sources

Accessed 25 July 2026 unless otherwise stated.

1. Association of British Insurers, average 2024 combined premium and 16.5 million policies in tracker: [More action needed to protect properties as adverse weather takes record toll on insurance claims in 2024](https://www.abi.org.uk/news/news-articles/2025/2/more-action-needed-to-protect-properties-as-adverse-weather-takes-record-toll-on-insurance-claims-in-2024/).
2. MoneySuperMarket home-insurance panel claim: [Home insurance](https://www.moneysupermarket.com/home-insurance/).
3. Go.Compare panel and product guidance: [How to choose the best home insurance](https://www.gocompare.com/home-insurance/guide/how-to-choose-the-best-home-insurance/).
4. Confused.com provider list: [Home insurance providers](https://www.confused.com/home-insurance/providers).
5. Compare the Market quote journey: [Home insurance](https://www.comparethemarket.com/home-insurance/).
6. Insurance Ireland, 2024 market figures: [Insurance Ireland Factfile 2024](https://insuranceireland.eu/wp-content/uploads/2026/01/Insurance-Ireland-Factfile-2024.pdf).
7. Insurance Ireland member directory: [General non-life members](https://insuranceireland.eu/consumer-information/directory-of-members/general-non-life-members/).
8. Central Statistics Office, 2022 dwelling and occupied-household count: [Census of Population 2022 – Housing](https://www.cso.ie/en/releasesandpublications/ep/p-cpr/censusofpopulation2022-preliminaryresults/housing/).
9. bonkers.ie current home-insurance partners: [Compare home insurance](https://www.bonkers.ie/compare-home-insurance/).
10. Chill intermediary panel: [Insurance companies](https://www.chill.ie/insurers/).
11. Compare Insurance Ireland provider examples and journey description: [House insurance](https://www.compareinsuranceireland.ie/house-insurance/).
12. Playwright browser support and update model: [Browsers](https://playwright.dev/docs/browsers).
13. Playwright network capture and proxy capabilities: [Network](https://playwright.dev/docs/network).
14. Playwright test agents: [Agents](https://playwright.dev/docs/test-agents).
15. Cloudflare, browser/session signals and headless-automation detection: [Bot scores](https://developers.cloudflare.com/bots/concepts/bot-score/).
16. FCA, price comparison website risks and product-feature emphasis: [TR14/11 – Price comparison websites in the general insurance sector](https://www.fca.org.uk/publications/thematic-reviews/tr14-11-price-comparison-websites-general-insurance-sector).
17. ICO, UK GDPR principles including minimisation, accuracy and storage limitation: [Guide to the data protection principles](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/).
18. Irish Data Protection Commission, data-protection principles: [Guidance on the Principles of Data Protection](https://www.dataprotection.ie/en/dpc-guidance/guidance-principles-data-protection).
19. Irish Data Protection Commission, DPIA guidance: [Guide to Data Protection Impact Assessments](https://www.dataprotection.ie/en/dpc-guidance/guide-data-protection-impact-assessments).

