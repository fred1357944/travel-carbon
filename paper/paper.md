---
title: "travel-carbon: distance-based Scope 3 Category 6 helpers for free-text Chinese university travel ledgers"
tags:
  - carbon-footprint
  - scope-3
  - business-travel
  - higher-education
  - Taiwan
  - OSRM
  - GHG-Protocol
  - Python
authors:
  - name: Hung-Yi Lai
    corresponding: true
    affiliation: "1"
affiliations:
  - name: "Fu Jen Catholic University, New Taipei City, Taiwan"
    index: 1
date: 12 July 2026
bibliography: paper.bib
repository: https://github.com/fred1357944/travel-carbon
# archive_doi: "10.5281/zenodo.XXXXXXX"  # set after Zenodo (see docs/JOSS_SUBMISSION.md)
---

# Summary

Higher-education institutions (HEIs) increasingly report greenhouse-gas (GHG) inventories that include employee business travel under the GHG Protocol Corporate Value Chain (Scope 3) Standard, Category 6 (*Business travel*) [@ghgprotocol_cat6]. When activity data are incomplete, organisations often rely on spend-based estimates. Distance-based methods improve data quality when trip distances and modes can be recovered, but many Taiwanese campuses store evidence as administrative Excel ledgers with free-text Traditional Chinese destinations, not structured travel-management feeds.

`travel-carbon` is an open-source Python package and companion desktop workflow that recovers destinations from free-text Chinese travel rows, estimates hybrid road and flight distances with Taiwan-specific island rules, multiplies distances by transparent screening emission factors, and optionally attaches Folium route maps as visual audit trails in the GUI. A library API (`estimate_trip`), command-line interface, and offline evaluation harness support reproducible checks without distributing personal data. The software is intended as a Category 6 activity-data sub-pipeline for HEI sustainability and finance staff, complementary to multi-scope campus carbon platforms.

# Statement of need

Academic and administrative travel can be a material share of campus climate inventories [@ciers2019; @vallsval2021; @kiehle2023]. Taiwanese HEIs are expanding ISO 14064-style organisational accounting practices that include business travel [@tsai2025]. In many East Asian administrative systems, the primary record is still a reimbursement workbook whose destination field is free text (district names, 台/臺 variants, multi-stop notes, missing values). Converting those rows into distance-based Category 6 estimates is often done by hand: staff re-type places into web maps, apply inconsistent factors, and lack per-trip visual evidence for internal review. Manual map look-ups are slow and hard to reproduce year-to-year; this operational claim is based on the development context of annual university travel ledgers rather than a formal multi-site time-and-motion study, which we treat as a limitation rather than a finished impact result.

Commercial carbon APIs and enterprise travel tools typically assume structured legs (airports, cabin class, ticketed modes). Open university-oriented tools such as the estimator of @auger2021, CO2UNV [@vallsval2022], and GES 1point5 [@mariette2022] serve important laboratory and multi-scope use cases, usually with structured activity inputs. `travel-carbon` targets the narrower but practical gap of Traditional Chinese free-text administrative ledgers plus Taiwan mainland versus offshore routing in one installable package—not as a claim of inventing university carbon accounting in general.

# State of the field

Prior open tools emphasise different layers of the same problem. GES 1point5 provides a standardised web application and national database for research-group footprints, including professional travel, with transparent methodology and optional aviation non-CO₂ options [@mariette2022]. CO2UNV offers a configurable multi-scope university carbon-footprint workbook [@vallsval2022]. @auger2021 demonstrates an open campus-oriented estimator. These systems document structured or form-based activity models in their public materials. We have not run a shared head-to-head benchmark against them on one Chinese free-text ledger; the comparative claim rests on their documented input assumptions, not empirical speed tests. A build-versus-contribute assessment: grafting free-text Chinese ledger parsing onto GES 1point5 would require changing its activity model from structured modes to raw administrative strings, while CO2UNV remains workbook-centric rather than a Python library for batch GIS-style distances. We therefore package a focused Category 6 distance-based sub-pipeline that can feed, rather than replace, broader inventory systems.

# Software design

Distance policy is hybrid by design. Mainland Taiwan road legs use optional OSRM routing on OpenStreetMap data, with a geodesic times 1.4 fallback when the public router is unavailable [@huber2016; @osrm]; the 1.4 factor is an operational heuristic documented in code and is not validated as a Taiwan-specific calibration. Offshore islands use geodesic flight distances from a domestic hub (Songshan by default); international legs use geodesic distances from Taoyuan airport hubs after city-to-hub mapping. A hardcoded gazetteer is preferred over live third-party geocoding so that offline tests remain deterministic and employee destination strings need not leave the machine; the cost is a hand-maintained coordinate table without per-entry provenance metadata.

Emission accounting follows the GHG Protocol Category 6 distance-based pattern (distance times mode factor). Shipped screening factors are operational defaults, not a line-item mapping to Taiwan MOENV organisation fuel-factor tables (kg/TJ). Among screening values, high-speed rail 0.034 kg/km aligns with a published product-CFP entry; a `taiwan_cfp` profile exposes lower car factors for sensitivity analysis. Unresolved destinations are classified as `unknown` with zero distance and a `resolved=false` flag rather than silently treated as international flights of length zero. Mode assignment from labels and distance thresholds is heuristic, not ticket-level truth.

# Functionality

The installable package exposes gazetteer data, free-text normalisation and trip-kind classification, hybrid distance builders, factor profiles, end-to-end `estimate_trip`, and an offline gold-CSV evaluation command. The repository also retains a Tkinter GUI for batch Excel workflows with route caches and Folium map export. Users should consult the README for installation and CLI examples; this paper does not duplicate full API documentation.

Default screening factors (kg CO₂e/km) include illustrative car/taxi 0.21, domestic air 0.133, international air 0.101, rail/HSR 0.034, and bus 0.065. Aviation non-CO₂ radiative forcing is omitted by default [@lee2021]. Users must recalibrate factors for formal ISO 14064-1 reporting.

# Quality assurance

Unit tests cover carbon arithmetic, gazetteer resolution, offline distances, factor loading, evaluation harness behaviour, and the unresolved-destination guard (48+ tests at v0.1.x). Continuous integration runs on Python 3.10 and 3.12. A synthetic gold set (`examples/sample_travel_gold_50.csv`) exercises mainland districts, character variants, islands, international hubs, empty fields, and unresolved junk strings. Offline evaluation should be read primarily as a regression-test pass rate on author-maintained labels, not as independent external validation: the same project authors maintain both classifier and labels. One intentional junk row checks that unresolved text remains `unknown` rather than a silent zero-kilometre international flight. Distance MAPE against independent mileages and precision/recall of free-text extraction on real institutional ledgers remain recommended future work. Real reimbursement workbooks are excluded from version control.

# Research impact statement

The public repository and installable package were released in July 2026. At the time of writing, `travel-carbon` has not yet been cited in an independent published inventory. Near-term research utility rests on reproducible artefacts available today: a documented Category 6 distance-based pipeline, CI-verified examples, and an offline evaluation harness. Operational motivation comes from university travel-ledger processing in a Fu Jen Catholic University sustainability-reporting setting; only synthetic examples are distributed. We intend to report anonymised institutional evaluation metrics after appropriate data-governance review.

# AI usage disclosure

Generative AI assistants (including GitHub Copilot CLI and multi-model manual review sessions documented under `docs/`) were used for code scaffolding, test generation, documentation drafting, adversarial paper review, and copy-editing during package extraction in July 2026. The corresponding author reviewed, executed, and validated generated code against the test suite and made emission-factor, architecture, and scope decisions. No AI tool is authorised to submit or respond to JOSS reviews without human approval.

# Acknowledgements

We thank the OpenStreetMap, OSRM, Folium, and Geopy communities. Institutional travel-ledger workflows at Fu Jen Catholic University motivated the design; only synthetic examples ship in the public tree.

# References
