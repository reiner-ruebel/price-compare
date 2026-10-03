# Household Insurance Price Comparison

## Lean Delivery and Effort Matrix — Version 2

**Prepared for:** ERGO UK and Ireland  
**Estimate date:** 25 July 2026  
**Estimate unit:** one person-day (MD) = eight working hours

## Objective

Run the owner’s fixed set of approximately 250 test cases once per week against:

- one comparison portal; and
- three direct competitors.

This produces approximately 1,000 target-specific quote journeys per week:

`250 test cases × 4 target websites = 1,000 journeys`

The cases are test data, not customer cases. They are supplied and owned by the owner and may be adjusted occasionally.

## Terminology

A **translation**—sometimes called a connector—is the target-specific part of the solution. It:

1. reads one owner test case;
2. maps its fields and values to one target website;
3. completes that website’s quote journey; and
4. extracts the result into the common output.

One portal and three competitors therefore require four translations. The pilot creates the first translation. The stand-alone operational version adds the remaining three.

If a competitor is replaced later, the new competitor normally requires one new translation. The shared application is retained.

## Effort matrix

| ID | Result | Classification | Creation (MD) | Maintenance (MD/month) | Comment |
|---|---|---|---:|---:|---|
| B1 | Agreed list of one portal and three competitors, with one target selected for the pilot | Pilot | **1** | — | May be supplied by the owner. If the supplier prepares it, the effort is one day. |
| B2 | Fixed set of approximately 250 test cases in an agreed input structure | Pilot | **0** | — | Supplied and maintained by the owner. Validation that the file can be read is included in B3. |
| B3 | Working end-to-end pilot for one target, including one translation and a result file | Pilot | **8** | — | Produces real results from owner test cases and supports a yes/no decision. The code is reused in B4. |
| B4 | Stand-alone operational application covering all four targets | Baseline continuation | **15** | **1–3 on demand** | Adds three translations, weekly batch execution, common output, basic logs, restart handling and expected-path tests. |
| B5–B6 | Portal-11 integration using existing Foundation tables, reporting, audit and artifact capabilities | Optional | **10** | **0–0.5 incremental** | Adds Portal persistence, DTO/table manifests, import/export/view/edit, query/filter/aggregate reporting and execution integration. It does not rewrite the four translations. |
| B7–B9 | Extended evidence, data-quality, traffic-control, security and privacy hardening | Optional | **10** | **0.5–1 on demand** | Combined optional assurance scope after the operational version is accepted. |
| B11 | Deployment to an agreed existing environment and production smoke check | Optional | **1** | — | Assumes the environment and required access already exist. |
| B12 | Counsel-ready factual description of the technical activity | Optional | **1** | — | Describes what the solution does for legal review; it is not legal advice. |

## Delivery decisions

### Pilot

The pilot is B1–B3:

- **8 supplier MD** if the owner provides B1 and B2;
- **9 supplier MD** if the supplier also prepares B1.

At the end of the eight-day technical pilot, the owner receives:

- a working translation for one selected target;
- results for the agreed owner test cases;
- the input and result formats;
- a list of target fields that could not be mapped or require an owner decision;
- observed run time and failure behaviour; and
- a recommendation to proceed, change the first target, or stop.

This is a genuine pilot and decision gate, not a paper study or throwaway prototype.

### Stand-alone operational version

B4 is **15 additional MD** after a successful pilot.

Cumulative effort is therefore:

| Outcome | Supplier creation effort |
|---|---:|
| One-target working pilot | **8–9 MD** |
| Four-target stand-alone operational version | **23–24 MD** |
| Four-target version plus Portal-11 integration | **33–34 MD** |
| All listed creation scope | **45–46 MD** |

## What B4 includes

- reuse of the pilot translation;
- three additional target translations;
- reading the owner’s fixed test-case file;
- running 250 cases against each of four targets;
- target selection and configuration;
- common result output with case, target, timestamp, result and status;
- basic failure classification and logs;
- safe restart of an interrupted batch;
- ordinary development tests and representative end-to-end runs; and
- concise operating instructions.

The test-case values may change without software work, provided the columns and answer meanings stay the same.

## What is deliberately on demand

The first operational version includes normal expected-path testing. The following are added only if the owner needs them:

- exhaustive edge-case and adversarial testing;
- extensive screenshot or raw-response evidence;
- automated detection of plausible but incorrect quotes;
- sophisticated traffic shaping, anomaly detection and circuit breakers;
- long-running soak and recovery testing;
- formal security/privacy assurance beyond normal implementation care; and
- unusual products, additional countries or materially different test-case fields.

These items can be delivered under B7–B9 or estimated as a smaller bounded change when the need is known.

## Change rules

- Changing case values or rows within the existing input structure normally requires no development.
- Adding a simple input field may be a small change; adding a new insurance concept may affect every translation.
- A normal target-page correction is maintenance.
- Replacing or adding a target normally requires one new translation. After the pilot, allow approximately **3–5 MD** for a standard journey; confirm the estimate when the target is known.
- A persistent access restriction, mandatory account/MFA step or completely redesigned quote journey is estimated separately.

## Assumptions and exclusions

- The owner provides valid, internally approved test cases and any controlled contact values required by a quote form.
- The quote journeys do not buy or bind policies.
- The estimate assumes publicly accessible, technically usable quote journeys.
- No CAPTCHA-solving service or bypass of authentication or technical restrictions is included.
- Infrastructure, hosting, network, third-party licence and legal-adviser costs are excluded.
- Maintenance is on demand, not a fixed monthly charge. A month without target changes may require no work.
