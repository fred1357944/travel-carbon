---
title: "From free-text reimbursement ledgers to Scope 3 Category 6 distances: an open workflow for Taiwanese higher-education business-travel carbon accounting"
author: "Hung-Yi Lai and Cheng-Chi Lee"
affiliation: "Center for Sustainable Development and Institutional Research, Fu Jen Catholic University, New Taipei City, Taiwan"
date: 2026-07-12
target_venues: "IJSHE (primary) — quality over speed"
status: "working draft — de-identified institutional process statistics feasible (center holds data); formal written approval required (non-author-only sign-off)"
bibliography: references.bib
---

# Abstract

**Purpose** — Higher-education institutions (HEIs) must increasingly quantify business-travel emissions under GHG Protocol Scope 3 Category 6 and ISO 14064-style organisational inventories. In many Taiwanese universities, activity evidence resides in free-text reimbursement Excel ledgers rather than structured booking extracts. This paper presents an open workflow and software package (`travel-carbon`) that recovers destinations from Traditional Chinese free text, estimates hybrid road/flight distances, and produces transparent distance-based CO₂e screening estimates with optional map audit trails.

**Design/methodology/approach** — We describe a distance-based Category 6 pipeline: gazetteer- and rule-based destination normalisation; OSRM road routing (optional) with geodesic fallback for Taiwan mainland trips; geodesic island and international flight legs; mode heuristics; and screening versus Taiwan product-CFP-oriented factor profiles. Quality assurance combines unit tests, continuous integration, and a synthetic gold set (*n* = 52) for trip-kind and mode-heuristic regression checks.

**Findings** — On the synthetic gold set, offline trip-kind and mode-heuristic accuracies both reach 1.0 as regression metrics (author-maintained labels). Screening and `taiwan_cfp` factor profiles produce different aggregate CO₂e on the same distances, illustrating factor sensitivity. Unresolved destinations are flagged as unknown rather than silent zero-kilometre international flights.

**Practical implications** — Sustainability and finance offices can batch-process Chinese free-text ledgers with inspectable open-source code, then recalibrate factors for formal inventory years.

**Originality/value** — Complements multi-scope HEI tools (e.g. GES 1point5, CO2UNV) by targeting Traditional Chinese administrative free-text ledgers and Taiwan-specific mainland/island routing in one installable package.

**Keywords** — higher education; Scope 3; business travel; carbon footprint; Taiwan; open-source software; GHG Protocol Category 6

**Paper type** — Research paper / tool-and-workflow case (working draft)

# 1. Introduction

Business travel is a material and often under-measured component of university greenhouse-gas (GHG) inventories [@ciers2019; @helmers2021; @kiehle2023]. Under the GHG Protocol, emissions from employee travel in third-party vehicles fall in Scope 3 Category 6 [@ghgprotocol_cat6; @ghgprotocol_scope3]. ISO 14064-1 provides organisational quantification and reporting guidance used by many Taiwanese HEIs [@iso14064_1_2018; @tsai2025].

Prior research documents academic flying’s contribution to campus footprints [@ciers2019; @wynes2018ubc; @wynes2019], policy gaps in university climate plans [@schmidt2022], and practice-based barriers to reducing academic air travel [@tseng2022; @schreuer2023; @sunley2025]. Reviews of HEI carbon-footprint methods highlight incomplete Scope 3 data and heterogeneous boundaries [@vallsval2021; @helmers2021; @deda2025].

Less attention has been paid to the **operational data path** from messy East Asian administrative ledgers—free-text destinations, character variants (台/臺), district names—to distance-based Category 6 activity data. Spend-based methods are common when distances are missing, but they can be sensitive to prices and poor for year-on-year operational management [@ghgprotocol_cat6]. This paper addresses that gap with an open workflow and software package designed for Taiwanese HEI contexts.

**Research questions.**  
*RQ1:* What technical and organisational steps are required to turn free-text Traditional Chinese reimbursement ledgers into auditable distance-based Category 6 activity data?  
*RQ2:* How sensitive are resulting screening totals to factor-profile choice and unresolved-destination handling?

# 2. Related work and research gap

## 2.1 HEI carbon inventories and travel

University carbon-footprint studies emphasise energy, commuting, and business travel [@vallsval2021; @kiehle2023; @helmers2021]. Air travel can dominate partial Scope 3 mobility totals at research-intensive campuses [@ciers2019; @helmers2021]. Mitigation research examines institutional manoeuvring room and sustainable travel policies [@schreuer2023; @sunley2025; @goerlinger2023]. Taiwanese HEIs applying ISO 14064-1 report that commuting and business travel are material yet data-constrained [@tsai2025].

## 2.2 Tools for campus and research carbon accounting

Open tools include GES 1point5 for research laboratories [@mariette2022], CO2UNV for configurable university footprints [@vallsval2022], and other open estimators [@auger2021]. These systems typically assume structured activity inputs. Commercial platforms and ICAO’s flight calculator [@icao_icec] address aviation with richer aircraft data, but rarely ingest free-text Chinese reimbursement rows.

## 2.3 Methodological issues in travel emissions

Category 6 methods include fuel-, distance-, and spend-based approaches [@ghgprotocol_cat6]. Aviation climate impact includes non-CO₂ effects [@lee2021; @jungbluth2019]. National conversion factors (e.g. UK DESNZ/DEFRA) [@defra_conversion_factors] and Taiwan MOENV fuel tables [@moenv_113_factors] versus product carbon footprints [@moenv_cfp] must not be conflated. Chinese toponym extraction research highlights free-text geo-resolution challenges [@kuai2020].

## 2.4 Gap

We find limited open methods that jointly (i) normalise Traditional Chinese free-text HEI travel destinations, (ii) apply Taiwan mainland road versus offshore flight policies, (iii) expose distance-based screening factors with explicit honesty about Taiwan statutory sources, and (iv) ship reproducible open-source software with automated tests. This paper presents such a workflow.

# 3. Methods

## 3.1 System overview

The `travel-carbon` package [@travel_carbon_software] implements:

1. **Destination recovery** — aliases, 台/臺 normalisation, district→city and city→airport maps [@kuai2020].  
2. **Distance estimation** — optional OSRM driving [@huber2016; @osrm]; geodesic×1.4 road fallback; geodesic island/international flights.  
3. **Mode heuristics and factors** — label- and distance-based mode assignment; screening versus `taiwan_cfp` profiles.  
4. **Audit artefacts** — optional Folium maps in the desktop GUI; `resolved` flags for unknown destinations.  
5. **Evaluation harness** — offline gold CSV scoring without personal data.

Origin defaults to Fu Jen Catholic University for mainland driving; Songshan and Taoyuan airports for domestic island and international legs, respectively.

## 3.2 Emission factors and accounting boundary

We follow GHG Protocol Category 6 distance-based calculation in form:

\[
E = \sum_i d_i \times EF_i
\]

Screening defaults shipped with the software are **operational** kg CO₂e/km values. They are **not** a direct mapping to Taiwan MOENV’s 2024 organisation fuel-factor gazette (kg/TJ) [@moenv_113_factors]. Product-CFP pkm factors [@moenv_cfp] provide closer Taiwan-facing sensitivity values for cars and high-speed rail; aviation remains uncertain and may require ICAO-style methods [@icao_icec] for formal inventories. Radiative forcing multipliers are omitted by default [@lee2021; @jungbluth2019].

## 3.3 Quality assurance design

Unit tests and CI (Python 3.10/3.12) cover pure functions. A synthetic gold set (*n* = 52) labels expected trip kinds (mainland/island/international/unknown) and expected mode substrings. Metrics are **regression accuracies**, not independent multi-rater validation. Unresolved free-text strings are required to classify as `unknown` with zero distance (under-reporting risk if misused without review of unresolved rows).

# 4. Results

> **Note on synthetic metrics.** Trip-kind / mode-heuristic scores of 1.0 on the author-maintained gold set are reported under **§3.3 Quality assurance** as regression checks, **not** as independent validation findings.

## 4.1 Factor sensitivity (workflow implication)

Applying `sensitivity_compare` and dual-profile batch runs shows that, once distances exist, inventory-like totals are **factor-dominated**: moving private-car factors from screening 0.21 to CFP-oriented 0.115 kg/km changes leg-level CO₂e substantially [@ghgprotocol_cat6; @moenv_cfp]. Full-ledger tornado-style tables (screening vs `taiwan_cfp`, optional aviation RFI scenarios citing [@lee2021; @jungbluth2019]) are the primary quantitative result of the current draft; absolute campus CO₂e totals are **not** claimed without an authorised de-identified institutional year.

## 4.2 Failure modes and unresolved-destination governance

Unresolved free-text destinations are classified as `unknown` with zero distance and `resolved=false` (package behaviour as of v0.1.x), so they do not silently enter international 0 km flight accounting. This creates an explicit **data-quality worklist** for offices: unresolved rate itself should be treated as a reportable quality indicator, not as automatic under-count acceptance. Gazetteer gaps remain a maintenance issue.

## 4.3 Institutional process statistics (placeholder)

*To be filled after data-governance approval:* de-identified process statistics for one academic year (resolution rate, unknown rate, trip-kind distribution, mode heuristic distribution, distance distribution)—**with or without** publishing absolute CO₂e totals.

# 5. Discussion

## 5.1 Implications for HEI sustainability offices

Distance-based Category 6 accounting is only as good as destination recovery and factor choice [@ghgprotocol_cat6; @deda2025]. Open workflows can improve transparency and auditability relative to opaque spreadsheet macros, provided unresolved rows and factor years are reviewed.

## 5.2 Relation to travel reduction agendas

Measurement tools do not by themselves reduce flying [@tseng2022; @schreuer2023]. They can, however, support policy monitoring and department-level feedback once activity data exist [@schmidt2022; @sunley2025].

## 5.3 Limitations

- Synthetic gold is not external validation; no MAPE against official mileages yet.  
- Public OSRM has no SLA; road factor 1.4 is uncalibrated for Taiwan.  
- Mode heuristics are not booking truth.  
- Institutional case results require data-governance approval before publication.  
- Single-author software release (2026) has short public history.  
- Companion education/adoption study (classroom + staff appraisals) is out of scope here and will be reported separately if conducted.

## 5.4 Future work

De-identified multi-year Fu Jen (or multi-campus) process statistics; factor tables versioned by inventory year; optional ICAO integration for aviation; usability evaluation of export formats for inventory appendices.

# 6. Conclusion

We presented an open, testable workflow for turning Traditional Chinese free-text HEI travel ledgers into distance-based Scope 3 Category 6 screening estimates with Taiwan-aware routing and explicit factor honesty. The package is available at https://github.com/fred1357944/travel-carbon. Application-journal readiness requires institutional case results beyond synthetic regression tests; the present draft is a methods-and-tool foundation for that next step.

# Acknowledgements

OpenStreetMap, OSRM, Folium, and Geopy communities. Fu Jen Catholic University sustainability-oriented travel-ledger workflows motivated development; only synthetic examples are distributed.

# AI usage disclosure

Generative AI tools (including GitHub Copilot CLI and multi-model reviews) assisted scaffolding, drafting, and adversarial critique. The author validated code and takes responsibility for scientific claims.

# References
