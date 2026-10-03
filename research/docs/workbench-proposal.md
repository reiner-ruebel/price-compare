# Proposal

Your mental model is good: **the valuable system is not the quote-bind API itself; it is the broker-submission-to-underwriting-case layer in front of it.** That is where data quality, workflow, communication, evidence, triage, and underwriter productivity live.

I would name this internally:

> **Broker Submission Intake & Underwriting Workbench Layer**

or shorter:

> **Submission Workbench**

That avoids sounding like you want to replace the quote-bind vendor.

------

## Satellite view

ERGO/JRP likely receives broker submissions in mixed form: email, attachments, forms, broker portals, maybe e-trade referrals. The workbench should turn that messy input into a **case**, enrich it, ask for missing information, prepare a structured quote-bind request, support referral decisions, and preserve a full audit trail.

This maps extremely well to TaskLogic’s own defined wedge: decision systems embedded into existing processes, using data integration, decision logic, workflow, and feedback loops.

------

# a. What does a user look like?

There is not one user. There are several personas.

## 1. Broker user / requester

This is the external person submitting or following up on a risk.

Typical needs:

- submit a property risk quickly
- avoid rekeying
- forward an email or upload documents
- check status
- answer missing-info questions
- receive quote / referral / decline / document requests
- see previous cases

Likely roles:

- broker account executive
- broker account handler
- wholesale broker
- scheme broker
- delegated-authority partner
- possibly coverholder / MGA partner, depending on ERGO’s structure

For your system, the broker should have:

- organization account
- named users
- permissions by branch/team
- case list
- upload/email submission channel
- status tracking
- message thread per case

## 2. Underwriting assistant / underwriting operations

This may be the most important internal user.

They do the “middle work” today:

- open emails
- read proposal forms
- inspect attachments
- chase missing information
- rekey data
- pre-check appetite
- prepare referral notes
- route to underwriter
- update broker

The workbench should save them the most time.

## 3. Underwriter

The underwriter should not be forced into admin work. Their main screen should show:

- risk summary
- extracted facts
- confidence indicators
- missing / conflicting data
- appetite result
- hazard / claims / contract context
- suggested next action
- full source evidence
- quote-bind payload preview
- referral notes
- communication history

They need control. The system can suggest, but the underwriter must approve important decisions.

## 4. Underwriting manager / portfolio owner

They care less about one case and more about the book.

Needs:

- submissions by broker
- quote rate
- bind rate
- decline/refer reasons
- cycle time
- risk quality
- accumulation / geography
- leakage: submitted but not quoted, quoted but not bound
- broker performance
- underwriter workload

## 5. Admin / product owner

Needs:

- manage products
- map fields
- configure required questions
- maintain appetite rules
- manage broker users
- manage status templates
- manage integrations
- audit changes

------

# b. What is the incoming data?

Think in three layers: **channel**, **document/input type**, and **business content**.

## Incoming channels

Likely channels:

- forwarded email
- email to dedicated submission mailbox
- web form
- broker portal upload
- uploaded PDFs / Word / Excel
- ACORD-style or London Market files, depending on segment
- quote-bind platform referral response
- e-trade system referral, for example from Acturis / Open GI / Applied / SSP-type workflows

Whitespace and PPL are more London Market placement-style platforms. Whitespace says brokers and underwriters can create submissions, collaborate, request/provide quotes, bind, sign and endorse contracts digitally.  Lloyd’s material describes PPL as the London Market electronic placing platform for quote, negotiate, bind and endorse business digitally.

For regional commercial/property-owner business, Acturis, Open GI, Applied, SSP, insurer portals, and broker emails are probably more relevant than PPL/Whitespace.

## Incoming document/input types

Common package may include:

- broker email
- statement of fact
- proposal form
- schedule of properties
- property owner questionnaire
- Excel property list / bordereau-like file
- claims experience
- current policy schedule
- expiring premium
- insurer renewal invite
- valuation / rebuilding-cost document
- photos
- survey report
- risk improvements / recommendations
- tenancy schedule
- construction details
- flood report, if broker already has one
- target premium or competitor quote
- sanctions / compliance information, if commercial entity

## Business content extracted

For property underwriting, likely fields include:

- insured name
- broker name / branch / contact
- risk address / property list
- postcode
- geocoded location
- property type
- occupancy / trade / tenant type
- owner-occupied / let / unoccupied
- residential / commercial / mixed portfolio
- construction
- year built / age
- number of units
- sum insured / buildings TIV
- contents / rent / liability covers
- loss of rent / alternative accommodation
- claims history
- inception date
- period of insurance
- expiring insurer
- expiring premium
- required cover sections
- excesses
- endorsements / special terms
- target commission
- broker requested terms
- referral reason
- urgency / deadline

For the first pilot, do **not** try to support every class. Pick one, for example:

> Property Owners — residential let / commercial let / mixed portfolio, one broker channel, new business submissions.

That is enough.

------

# c. What additional data needs to be looked up, digested, or merged?

This is where Corvendor/TaskLogic can be valuable.

## External enrichment

Likely enrichment:

- address normalization
- postcode validation
- geocoding
- flood risk
- subsidence risk
- storm / freeze / weather peril
- crime / theft risk
- fire brigade / distance to fire station, if relevant
- listed building / conservation area
- property age / construction indicators
- rebuild-cost estimate
- occupancy / company data
- sanctions / PEP / financial crime checks for commercial insureds
- Companies House data
- planning / property classification data
- EPC data where useful
- environmental risk
- portfolio accumulation by geography

## Internal ERGO/JRP data

This is more important than external data long term:

- existing policies
- previous quotes
- declinatures
- claims history
- broker performance
- underwriter decisions
- current appetite guides
- authority limits
- pricing model outputs
- claims ratio by product/broker/segment
- endorsements / clauses used historically
- renewal performance
- complaint / service quality indicators
- bordereaux / delegated authority reports
- existing customer / duplicate risk detection

## Derived / digested data

The middle layer should create “case intelligence,” not just store files:

- completeness score
- data confidence score
- missing information list
- conflict list, for example different sums insured in email vs PDF
- appetite pre-check
- likely referral reason
- triage priority
- underwriter workload routing
- broker quality score
- similarity to previous cases
- recommended next question to broker
- generated underwriting summary
- quote-bind readiness score

This is a strong phrase:

> **Quote-bind readiness**

It means: “Can this case be sent to the quote-bind API safely, or must we ask / enrich / refer first?”

------

# d. What does the API need? Which APIs are mostly used in the UK?

You need to separate three API categories.

## 1. Broker distribution / e-trade platforms

These are the channels where brokers already work.

Relevant UK names include:

- **Acturis** — describes itself as a leading commercial lines broker platform with the largest commercial e-trade panel in the UK.
- **Open GI / imarket / IHP** — Open GI positions Insurer Hosted Pricing as real-time pricing, reporting, enrichment integration, fraud rules, and integration with software houses. Polaris describes Open GI as a major UK/Ireland personal and commercial general insurance system provider.
- **SSP / imarket** — Polaris describes SSP + imarket as a panel allowing brokers to source comparative quotes and trade commercial business with back-office integration; its table includes Property Owners as a traded product.
- **Applied Systems / Applied Epic / Applied Commercial** — Applied says its broker connectivity automates rating and fulfilment across personal and commercial lines and reaches brokers through integrated panels. Applied Commercial says it automates commercial quoting workflows and reduces rekeying into back-office systems.
- **CDL** — relevant particularly in personal lines / broker software contexts, but you would need to verify relevance for their exact ERGO/JRP product line.
- **Insurer portals** — many insurers maintain their own broker portals.
- **PPL / Whitespace** — more London Market / complex placement oriented; relevant if their target business sits there. Lloyd’s describes PPL as the London Market e-placing platform; Whitespace supports creating submissions, collaboration, quote requests, binding and endorsements.

## 2. Quote-bind / policy admin / rating APIs

These are likely the licensed platforms ERGO may choose.

Names to know:

- Open GI IHP / IHP Plus
- Acturis insurer connectivity / e-trade integrations
- Applied broker connectivity
- Genasys
- Buckhill
- CDL
- SSP
- CGI Insurance Market Manager
- possibly proprietary ERGO/JRP platform
- possibly a specialist MGA / London Market system

Genasys, for example, advertises policy/claims/billing, quote-and-bind, workflow, dashboards, webhooks, and many REST API endpoints for London Market / MGA / carrier operations.  Buckhill positions its quote-bind platform as API-driven for Lloyd’s insurers, brokers and MGAs.

The important point: **you do not need to own this part**. You need the quote-bind API contract.

## 3. Enrichment APIs

The workbench may need APIs for:

- address lookup
- geocoding
- Companies House
- peril/risk data
- claims/internal data warehouse
- document extraction/OCR
- email integration
- identity/access management
- notifications
- sanctions checks

## What does the quote-bind API need?

Typically, it will need a structured payload containing:

- product / scheme / binder identifier
- transaction type: quote, referral, bind, MTA, renewal
- broker identifier
- insured details
- risk address(es)
- occupancy / business activity
- property characteristics
- sums insured / limits
- cover sections
- inception date / term
- claims history
- optional covers
- excesses
- commission
- endorsements / conditions
- referral flags
- enriched risk attributes
- attachments / evidence references
- user / audit metadata

The vendor will define the exact shape. Your ask to ERGO should be very direct:

> “Please give us the quote-bind API input specification, mandatory/optional fields, validation rules, referral rules, sample accepted payloads, sample rejected payloads, and example documents/emails from real submissions.”

That is the first serious discovery step.

------

# e. Domain language — use these terms

Use language that sounds like insurance operations, not generic software.

## Core entities

- **Submission** — what the broker sends.
- **Case** — internal managed work item created from a submission.
- **Risk** — the insured exposure being assessed.
- **Insured** / **policyholder** — the customer.
- **Broker** — intermediary submitting the business.
- **Underwriter** — decision owner.
- **Product** / **scheme** / **facility** — the insurance offering.
- **Class of business** — property owners, commercial combined, liability, etc.
- **Quote** — offered terms before binding.
- **Bind** — acceptance of quote into coverage.
- **Policy** — issued contract.
- **Referral** — case cannot be auto-quoted and needs underwriting review.
- **Decline** — risk outside appetite.
- **Appetite** — what ERGO/JRP wants to write.
- **Authority limit** — what an underwriter or delegated partner may approve.
- **Endorsement / clause / condition** — contractual modifications.
- **Excess** — deductible.
- **Limit / sum insured / TIV** — amount insured.
- **Premium** — price.
- **Commission** — broker remuneration.
- **Bordereau** — structured periodic report/list of policies/claims/premiums, common in delegated authority.
- **MTA** — mid-term adjustment.
- **Renewal** — continuation after policy period.
- **FNOL** — first notification of loss, claims side.
- **Claims experience** / **loss history** — prior claims.
- **Exposure** — what is at risk.
- **Accumulation** — concentration of exposures, often geographic/peril related.

## Workbench terms

These are good product terms:

- **Submission intake**
- **Case creation**
- **Data extraction**
- **Data enrichment**
- **Completeness check**
- **Quote-bind readiness**
- **Appetite pre-check**
- **Referral triage**
- **Underwriting summary**
- **Evidence pack**
- **Broker clarification**
- **Case status**
- **Audit trail**
- **Decision log**
- **Source-of-truth case record**
- **Structured risk profile**

Avoid saying “LLM makes the decision.” Say:

> **LLM-assisted extraction, summarisation, clarification drafting, and evidence navigation.**

That is much safer and more credible.

------

# f. Extra ideas based on your concept

## 1. Do not start with “portal”

The portal is standard. The differentiator is not registration, upload, login, status. Those are necessary, but not the core.

The core is:

> messy broker input → structured risk profile → quote-bind-ready case → underwriter decision support.

## 2. Build around a case timeline

Every case should have a timeline:

- submission received
- documents parsed
- missing fields identified
- enrichment completed
- broker clarification sent
- response received
- underwriter reviewed
- quote requested
- quote returned
- quote sent to broker
- bound / lost / declined / expired

This timeline becomes reporting gold.

## 3. Add “missing info automation”

This is probably a high-value pilot:

- extract required fields
- compare with quote-bind required schema
- detect missing fields
- generate broker email:
  - “Please confirm occupancy”
  - “Please provide claims history”
  - “Please confirm rebuilding sum insured”
- track response
- update case

This alone may save serious time.

## 4. Add “evidence linking”

Underwriters must trust extracted data.

For every extracted field:

- value
- source document
- page / email paragraph
- confidence
- manually confirmed yes/no

Example:

| Field                | Value                 | Source            | Confidence |
| -------------------- | --------------------- | ----------------- | ---------- |
| Building sum insured | £2.4m                 | Proposal PDF p.3  | 91%        |
| Occupancy            | Residential let       | Broker email      | 84%        |
| Claims last 5 years  | 2 water damage claims | Claims attachment | 78%        |

This is far more important than flashy AI.

## 5. Add “conflict detection”

Very valuable:

- email says £2.5m sum insured
- schedule says £2.0m
- proposal says unoccupied
- email says tenanted
- postcode invalid
- inception date missing
- insured name differs from company record

Conflict detection is underwriter productivity.

## 6. Add “decision log”

For compliance and internal learning:

- who decided
- when
- based on which information
- which appetite rule triggered
- quote-bind request payload version
- manual override reason
- final outcome

This later becomes model training data.

## 7. Add “broker quality reporting”

Over time, ERGO will learn:

- which brokers send complete submissions
- which bind after quote
- which submit poor-fit risks
- which generate profitable business
- which cause operational burden

That is business value.

## 8. Build “API-adapter-first”

Even before the final quote-bind vendor is chosen, you can design an adapter boundary:

```
Submission Workbench
   → Internal Structured Risk Profile
      → QuoteBindAdapter
         → Vendor A / Vendor B / Manual Export
```

This protects ERGO from vendor uncertainty.

## 9. Don’t let LLM sit in the critical path too early

Use LLM for:

- classification
- extraction assistance
- summarisation
- suggested questions
- comparing documents
- drafting broker emails
- underwriter Q&A over case documents

Do not initially use LLM for:

- final acceptance
- final pricing
- binding authority
- uncontrolled broker communication
- unreviewed regulatory explanations

------

# g. Findings / risks that could affect the project

## 1. Vendor lock-in risk

If they choose a quote-bind vendor later, your system must not depend on one vendor’s payload too early. Build a neutral internal risk profile first.

## 2. Broker channel conflict

If brokers already work inside Acturis/Open GI/Applied/SSP, forcing them into another portal may fail. Acturis stresses embedded broker workflow and e-trade connectivity; Applied stresses automated quote-bind inside broker workflows; Open GI IHP stresses integration with software houses.

So the workbench should support **email-first and integration-ready**, not “everyone must use our portal.”

## 3. “Unclear requirements” is normal here

They do not know what they want because the real object is a workflow, not a screen. You can help by producing:

- current-state workflow
- future-state workflow
- case data model
- quote-bind readiness checklist
- vendor-neutral payload model
- pilot scope for one product line

## 4. Compliance / auditability is not optional

The more AI touches underwriting, the more they will care about:

- explainability
- audit logs
- source evidence
- human approval
- role-based access
- data retention
- GDPR
- model governance

## 5. Data warehouse access may be harder than expected

Internal claims/contracts data sounds obvious, but may be messy:

- different systems
- inconsistent keys
- broker names not normalized
- address duplicates
- old policy systems
- claims data not directly linked to submissions
- GDPR / purpose limitation concerns

Make “internal data readiness” a discovery workstream.

## 6. Product scope can explode

Property insurance can quickly branch into:

- residential let
- commercial let
- mixed portfolio
- unoccupied property
- DSS tenants
- non-standard construction
- flood/subsidence risk
- multiple locations
- liability add-ons
- schemes
- renewals
- MTAs

Pilot must choose one.

## 7. The middle layer may be more valuable than quote-bind

Open GI’s IHP material says insurer-hosted pricing helps control pricing, enrich products, access data, support compliance, and avoid data leakage.  That reinforces your instinct: the value is not only “get a quote.” It is control, data, audit, and improvement.

------

# Recommended first ERGO/JRP discovery questions

Use these. They are concrete and non-threatening.

1. Which product/class should be the first candidate? Property Owners? Residential let? Commercial let? Mixed portfolio?
2. What are the top 20 fields required before an underwriter can quote?
3. What are the top 10 reasons submissions are referred, delayed, declined, or chased?
4. What channels do submissions arrive through today?
5. Can we see 20 anonymized real submissions, including emails and attachments?
6. Which broker systems matter most: Acturis, Open GI, Applied, SSP, portal, email?
7. Which quote-bind/rating platform is being considered?
8. Can we get the API schema or at least sample payloads?
9. What internal systems hold policy, claims, broker, and appetite data?
10. Who owns final underwriting authority?
11. What communication to brokers may be automated, and what must be approved?
12. What audit/regulatory evidence is required?
13. What is the current cycle time from submission to quote?
14. What percentage of cases are incomplete on first receipt?
15. What is the target improvement: speed, conversion, risk selection, expense ratio, broker experience, or data capture?

------

# The strongest pilot proposal

I would pitch this:

## **Pilot: Broker Submission Intake & Quote-Bind Readiness**

### Scope

One product line, one broker channel, 50–100 historical/anonymized submissions.

### Deliverable

A vendor-neutral case workbench that:

- receives email/upload/form submissions
- creates a case ID
- extracts required fields
- detects missing/conflicting data
- enriches address/risk data
- generates underwriter summary
- creates broker clarification draft
- prepares quote-bind-ready structured payload
- logs all evidence and decisions
- provides basic reporting

### Success metrics

- % fields auto-extracted
- % missing data detected
- reduction in manual rekeying
- reduction in time-to-ready-for-underwriter
- reduction in broker chase cycles
- underwriter satisfaction
- quote-bind payload completeness

This is narrow enough to be credible and valuable enough to matter.