# Current owner goal

Recorded on 3 October 2026. Build an **internal assessment tool** and publish its
results first, rather than supplying the tool to the owner.

The report must answer:

1. Which price-comparison portals and direct insurance competitors can provide
   data through ordinary Python requests, or Python with Playwright?
2. Which competitor brands/products does each portal actually return? Show a
   portal-by-competitor coverage matrix and distinguish a published panel from
   offers returned for the tested case.
3. Which competitors also have a usable direct route, adding coverage or a useful
   independent comparison?
4. How credible is continued access? Give a strict score and show the evidence
   and limitations behind it; a one-off successful quote is insufficient.

## Starting scope and existing evidence

Earlier documents concern UK home insurance, with Ireland as a secondary market;
the German HUK source is a technical reference. Confirm country, product, target
list and permitted test cases before live journeys. Begin useful independent
work by inventorying the research and building the assessment schema/report.

The Lemonade collector was observed to retrieve a premium on two journeys for
one supplied case on 7 September 2026. Treat it as historical observed evidence.
Do not label an untested portal or brand as accessible, blocked, or supported.
Keep quoted products, broker brands and underwriting entities distinguishable.

## Proposed strict score: 0–100

This is a proposed rubric for owner review, not an established industry standard
or a guarantee of future availability. Report individual dimensions and an
evidence grade alongside the total:

| Dimension | Maximum | Full-credit evidence |
| --- | ---: | --- |
| Access route and permission clarity | 20 | Documented/permitted route with known limits and account requirements |
| Actual data completeness | 20 | Premium, period, cover amounts, excesses, dates and offer/brand identity captured |
| Reproducibility | 20 | Repeated authorized runs across representative cases and separate dates |
| Maintainability | 15 | Clear adapter, validation, failure detection and manageable dependencies |
| Operational resilience | 15 | Measured success rate/latency, explicit failure handling and recovery path |
| Incremental competitor coverage | 10 | Verified useful panel/direct coverage without double-counting brand variants |

Apply conservative caps:

- Public research only: **not live-verified**, maximum 25/100.
- One successful quote/case: maximum 45/100.
- Repeats on the same day and case only: maximum 60/100.
- Unknown permission/terms or material missing comparability fields: maximum
  50/100; show the uncertainty explicitly.
- A CAPTCHA, access-denied response, login/paywall, or restricted interface is a
  stop/review condition. Do not work around it or confuse it with technical failure.

Use `not assessed` when evidence is absent. Record points separately from the
cap applied, and include source URLs, observed dates, case/run identifiers,
route type, returned-field evidence and failure classification. Do not publish
private input data, cookies, account details or full session captures.

## Suggested first delivery

Create a target registry, evidence records, scoring/report generator and offline
fixtures, then produce a dated initial report from current public research plus
clearly labelled historical Lemonade evidence. State precisely what remains to
be tested. Agree a bounded live test plan before expanding collection.

The owner requested results soon. Prefer a small useful report and transparent
unknowns over invented coverage or an unfinished large integration. Portal
integration, scheduled/batch collection and production hosting are later scope.
