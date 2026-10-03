# Household Insurance Price Comparison

## Internal Delivery Explanation — Version 2

**Date:** 25 July 2026  
**Related offer:** `price-comparison-effort-matrix-external-v2.md`

## 1. Why the estimate changed

The original 100+ MD estimate was too large for the scope now agreed. It assumed a general production platform with:

- supplier-owned market and scenario design;
- flexible risk and product schemas;
- separately priced target connectors;
- extensive evidence and wrong-price controls;
- production resilience and security work;
- multiple UAT cycles;
- deployment and legal documentation; and
- the possibility of new countries and arbitrary cases.

The clarified scope is much smaller:

- the owner supplies a fixed set of approximately 250 test cases;
- the same cases are run weekly;
- there are four known target websites;
- the first target is proven in an eight-day pilot;
- the pilot code is retained;
- the stand-alone version is deliberately simple;
- normal expected-path tests are included;
- extended edge testing and hardening are on demand; and
- Portal-11 already supplies generic tables, reports, audits and artifacts.

Under those assumptions, **23–24 MD for a four-target stand-alone version is a reasonable estimate**.

## 2. Calibration against Portal-11 delivery

The Portal-11 Block-011 File Manager was used as the delivery benchmark requested by the developer.

Between 21 and 24 July 2026, slices 088–092 delivered or exercised:

- Foundation manifest, permissions and scope;
- explorer, tree, search and list/grid behaviour;
- create, rename, copy, move, delete and bulk-selection operations;
- acquisition, upload, download and range handling;
- internal file/folder sharing;
- bounded folder ZIP;
- image preview;
- recycle, undo and recent activity;
- authenticated notification composition; and
- broad focused application, UI and integration tests.

The retained ledgers show that the main capability was developed quickly with substantial day-to-day test coverage. The final authenticated stabilization cycle still identified bounded presentation and identity-format issues, while complete edge/human acceptance remained separate.

That is the correct model for this offer:

- deliver the useful operational capability quickly;
- include tests for the normal expected paths;
- correct ordinary defects found during delivery; and
- add exhaustive edge testing only when requested or when a concrete risk justifies it.

Portal-11 also changes the integration estimate. We do not need to build generic table browsing, filtering, aggregation, import/export, artifacts and audit mechanisms again. We only need to declare the price-comparison data and connect the execution workflow to those existing capabilities.

## 3. Work unit: translation versus connector

The earlier document used the word **connector**. For this project, **translation** is clearer and matches the supplied HUK example.

Each target translation contains four things:

1. **Input mapping**  
   It maps the owner’s common test-case fields to the questions and answer values used by one target.

2. **Journey execution**  
   It navigates the target form, supplies the answers and reaches the quote result.

3. **Result translation**  
   It extracts price, result status and the agreed target output into the common format.

4. **Target-specific tests**  
   It proves representative owner cases against that journey and detects an obvious page or mapping failure.

For one portal and three competitors, four translations are required.

The pilot delivers translation 1. B4 adds translations 2–4. If a competitor changes, the application remains and only the target-specific translation is replaced.

Some targets may expose a stable browser API that makes the implementation shorter. Others may require full browser automation. The pilot decides the method based on the actual target; it should not promise one technical route in advance.

## 4. Volume and test cases

The weekly workload is:

`250 cases × 4 targets = 1,000 quote journeys`

The application-development effort is driven mainly by the four different journeys, not by whether 250 or 1,000 rows are read.

Running 1,000 journeys instead of 250 affects:

- elapsed run time;
- permitted parallelism;
- failure and retry count; and
- the chance of a target applying a restriction.

It does not require four times the application code.

The owner owns the case content. Normal changes to row values are data maintenance, not software development. Software work starts when:

- a new column or answer meaning is introduced;
- an existing answer is no longer accepted by a target;
- a new product type changes the journey; or
- a case requires a branch not supported by the existing translation.

## 5. Detailed delivery plan

### B1 — Target brief: 1 MD

#### Purpose

Remove ambiguity about which websites and quote products are in scope.

#### Work

- identify one comparison portal and three direct competitors;
- identify the exact public quote URL for each;
- state the required product, such as combined buildings and contents;
- choose one target for the pilot;
- record known access or geographic requirements; and
- record the output fields the owner wants to compare.

#### Deliverable

A short target brief and ordered implementation list.

#### Ownership

The owner can provide this directly. If the supplier facilitates the selection and records it, allow one day.

### B2 — Owner test cases: 0 supplier MD

#### Purpose

Provide the fixed input used by the solution.

#### Owner deliverable

A CSV or equivalent table containing:

- stable case identifier;
- one row per test case;
- agreed column names;
- allowed values;
- controlled contact data if a target requires it; and
- enough information to answer the selected target journeys.

The owner is responsible for the business validity and approval of the test data.

#### Supplier boundary

B3 checks that the file can be read and identifies missing mappings. B2 does not ask the supplier to redesign or statistically optimise the cases.

### B3 — One-target end-to-end pilot: 8 MD

#### Purpose

Prove that one real target can be automated with the owner’s actual test cases and that the output is useful.

#### Indicative eight-day sequence

| Day | Work |
|---:|---|
| 1 | Inspect the owner file and supplied HUK example; confirm the first target, journey and result fields. |
| 2 | Map owner fields and allowed values to the target questions; record missing or ambiguous answers. |
| 3–4 | Implement the first target translation and reach a quote result with representative cases. |
| 5 | Implement common result capture, case/target identity, status and basic log output. |
| 6 | Run a representative set and then the agreed case file; measure run time and classify normal failures. |
| 7 | Correct delivery defects, repeat failed expected paths and verify repeatability of the output format. |
| 8 | Produce the result pack, operating note, demonstration and proceed/change-target/stop recommendation. |

The day allocation is indicative. Work moves between days as the target journey is understood.

#### Pilot deliverables

- working source code for the first translation;
- runnable pilot command;
- input reader;
- result file linked to owner case IDs;
- basic error/log output;
- sample or full agreed pilot run;
- mapping and limitation note;
- observed execution time; and
- owner walkthrough.

#### Decision gate

The pilot supports one of three decisions:

- **Proceed:** the target works, output is useful and the remaining three translations can be estimated with confidence.
- **Change first target:** the approach is sound, but that portal/competitor is unsuitable.
- **Stop:** the result is not useful or the journeys are not technically workable within the intended effort.

The pilot is not discarded if work continues. Its translation, input reader and output model are the first part of B4.

### B4 — Four-target stand-alone operational version: 15 additional MD

#### Purpose

Turn the pilot into the simple weekly tool the owner asked for.

#### Effort breakdown

| Work | MD | Explanation |
|---|---:|---|
| Three additional target translations | 9 | Approximately three days each after the pilot has established the pattern. |
| Shared batch runner and configuration | 3 | Select targets, read cases, schedule/control execution, restart an interrupted run and combine output. |
| Result completion, operating instructions and expected-path tests | 3 | Common statuses, representative end-to-end checks, output validation and handover. |
| **Total** | **15** | Additional to B3 |

This is an allocation, not a contractual cap per translation. A simple target may take less and a more difficult target more, while the total remains the working estimate unless the pilot reveals a material obstacle.

#### Stand-alone deliverable

The owner can:

1. update or replace rows in the test-case file;
2. start the weekly run;
3. select all or individual targets;
4. see progress in a simple console/log form;
5. restart an interrupted run without discarding completed results;
6. obtain one common result file; and
7. distinguish quote, no-quote, validation failure, timeout and technical failure.

The stand-alone version does not require a custom management UI.

#### Included testing

- input file and required-column checks;
- representative case per supported path;
- successful result extraction;
- ordinary no-quote/validation result;
- target timeout or page failure;
- interrupted-run restart;
- output row/case/target association; and
- full agreed batch smoke run.

Defects found in these expected paths during delivery are included.

#### Deliberately excluded from B4

- exhaustive combinations of all case fields;
- rare browser/network races;
- long soak and disaster recovery tests;
- sophisticated wrong-price detection;
- adversarial access/security testing;
- screenshot/raw-response evidence for every case;
- formal privacy/security assurance;
- high-availability operation; and
- automated self-repair after a target redesign.

These are optional or on-demand assurance tasks.

## 6. Optional tasks

### B5–B6 — Portal-11 integration: 10 MD

#### Why ten days is credible

Portal/Foundation already provides the generic machinery. The price-comparison work should supply domain data and execution integration, not recreate a table/report product.

#### Effort breakdown

| Work | MD | Explanation |
|---|---:|---|
| Price-comparison entities, DTOs and Foundation table/report manifests | 2 | Run, case, target and result projections with columns, filters and aggregates |
| Persistence and migration | 2 | Tables and repository/adapters for run/result data |
| Execution integration | 3 | Start a run, connect to the translation engine, store status/results and expose artifacts |
| Portal composition | 2 | Import/export/view/edit, query/filter/aggregate and result/audit presentation using existing components |
| Expected-path tests and operating note | 1 | Focused domain, API and UI composition checks |
| **Total** | **10** | Does not reimplement translations |

#### Portal deliverable

- upload/import and maintain owner cases;
- start and inspect a run;
- persist case-target results;
- table view with query, filter, sort and aggregates;
- export results;
- artifact references for generated files;
- normal Portal audit coverage; and
- permissions/presentation consistent with existing Foundation patterns.

The execution engine may remain Python behind a controlled API/process boundary or be implemented with .NET Playwright. B3 should settle the lowest-effort boundary. Portal integration does not require translating working target logic into a second language.

### B7–B9 — Extended controls: 10 MD

This combines the former evidence, data-control, traffic-control, security and privacy rows.

Indicative allocation:

| Work | MD |
|---|---:|
| Additional evidence capture and traceability | 3 |
| Result sanity checks and anomaly handling | 3 |
| Improved retry/rate limits/circuit stop and operational controls | 2 |
| Security/privacy/retention refinements and edge tests | 2 |
| **Total** | **10** |

The exact allocation should follow observed pilot risks. For example, if the target always returns a clear structured result, extensive screenshot evidence may have little value; if plausible wrong results occur, data checks deserve more of the effort.

### B11 — Deployment: 1 MD

Assumes an agreed existing environment.

Includes:

- package/release;
- environment configuration;
- one deployed smoke run;
- verification of output location; and
- concise start/stop note.

Infrastructure procurement, firewall/owner-IT delays and creation of a new hosting platform are not included.

### B12 — Factual legal-review description: 1 MD

Includes:

- purpose and scope;
- target journeys and frequency;
- categories of test data submitted;
- results and technical evidence retained;
- execution location and operators;
- explicit non-purchase boundary;
- stop conditions; and
- questions requiring counsel approval.

It is a technical activity description, not a legal opinion.

## 7. Maintenance and target changes

Maintenance is expected to be event-driven.

| Change | Expected treatment |
|---|---|
| Owner edits case values or rows without changing the schema | No development |
| Minor input column or allowed-value change | Usually up to 1 MD, depending on affected translations |
| Small target label/selector/result-layout change | Normal maintenance, often 0.5–1.5 MD |
| Material target journey redesign | Estimate after inspection |
| Replace or add one standard competitor | New translation, normally 3–5 MD |
| New product or country | Separate scope because questions and result meanings change |

For four stable targets, retain an indicative **1–3 MD/month on-demand average**, not a fixed retainer. Some months may be zero. A month containing a major target change may be higher.

## 8. Technical choices

### Python and Playwright

The likely stand-alone choice:

- aligns with the supplied HUK reference and developer experience;
- keeps CSV handling simple;
- supports full browser journeys where necessary; and
- can later be invoked from Portal through a small boundary.

### Direct HTTP/API call

Use only when the pilot finds a stable and appropriate target endpoint. It may be quicker than browser automation, but a private endpoint can change without warning.

### .NET Playwright

Reasonable if the owner decides before B3 that all execution must live directly inside Portal. It should be a deliberate single implementation, not a rewrite after completing Python.

### AI

Not required for the fixed 250-case scope. AI does not remove the four translations. It may later help diagnose a changed page, but deterministic translations are simpler to test and explain.

## 9. Acceptance boundary

The operational version is accepted when:

- all four configured targets can run representative owner cases;
- the agreed 250-case file can be read;
- the weekly four-target batch can be started;
- every attempted journey produces a quote/result or a clear failure status;
- output rows remain tied to the correct owner case and target;
- an interrupted run can be continued safely;
- normal expected-path tests pass; and
- the owner completes the agreed walkthrough.

Acceptance does not assert that every insurer must quote every test case or that a third-party website will remain unchanged.

Extended edge assurance remains available on demand at a reasonable bounded effort.
