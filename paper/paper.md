---
title: "A desktop pipeline for distance-based Scope 3 Category 6 travel carbon accounting from free-text Chinese university ledgers"
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
  - name: Hung-Yi Lai  # Chinese: 賴弘翌
    # orcid: 0000-0000-0000-0000  # [PLACEHOLDER]
    corresponding: true
    affiliation: "1"
  # - name: "[PLACEHOLDER co-author]"
  #   affiliation: "1"
affiliations:
  - name: "Fu Jen Catholic University, New Taipei City, Taiwan"  # [PLACEHOLDER: confirm department / Independent]
    index: 1
date: 11 July 2026
bibliography: paper.bib
# repository: https://github.com/ORG/REPO  # [PLACEHOLDER]
# archive_doi: 10.5281/zenodo.XXXXXXX  # [PLACEHOLDER]
---

# Summary

Higher-education institutions (HEIs) increasingly report greenhouse-gas (GHG) inventories that include business travel under the GHG Protocol Corporate Value Chain (Scope 3) Standard, Category 6 [*Business travel*](https://ghgprotocol.org/sites/default/files/2022-12/Chapter6.pdf). When trip activity data are incomplete, many organisations fall back on spend-based estimates. Distance-based methods improve activity-data quality when trip distances and modes can be recovered, but Taiwanese university finance and sustainability offices often hold travel evidence only as **administrative Excel ledgers with free-text Traditional Chinese destinations and purposes**, not as structured booking extracts from a travel-management company.

This software provides an open-source **desktop pipeline** (Python, Tkinter) that (i) normalises destination strings from Chinese free-text travel reimbursement records using rule- and gazetteer-based parsing (including common 台/臺 variants and hierarchical district-to-city and city-to-airport mappings); (ii) estimates trip distances with a Taiwan-oriented hybrid policy—road network distances via the public [OSRM](http://project-osrm.org/) service for mainland Taiwan routes from a configurable campus origin (default: Fu Jen Catholic University), and geodesic (great-circle) distances for offshore-island and international air legs via airport hubs; (iii) attaches **route maps** (Folium / OpenStreetMap, with optional PNG screenshots) as visual audit trails; and (iv) multiplies distances by **transparent, simplified per-kilometre emission factors** to produce indicative CO₂e totals and mode summaries in Excel exports, aligned in method with GHG Protocol Scope 3 Category 6 **distance-based** calculation (not a certified product footprint or statutory inventory engine).

The tool is aimed at HEI administrators and sustainability staff who must turn messy annual ledgers into reproducible activity data and documentation for internal assurance or third-party verification workflows. It is complementary to laboratory- or campus-wide carbon platforms rather than a replacement for full multi-scope inventories.

# Statement of need

Academic and administrative travel can be a material share of campus climate inventories [@ciers2019; @vallsval2021; @kiehle2023]. Taiwanese HEIs are also expanding ISO 14064-style organisational accounting practices for business travel [@tsai2025]. In practice, Category 6 reporting quality is limited by **data form**: many campuses store reimbursement rows with free-text destinations rather than machine-readable itineraries. Manual map look-ups are slow, hard to audit, and inconsistent across years.

Commercial carbon APIs and enterprise travel tools typically assume structured legs (origin–destination airports, cabin class, ticketed modes). Open tools for university carbon estimation—such as the open-source campus estimator of @auger2021, the configurable multi-scope **CO2UNV** framework [@vallsval2022], and **GES 1point5** for research-group footprints including professional travel [@mariette2022]—serve important European and laboratory-oriented use cases, often with structured activity inputs or broader inventory scopes. They do not, to our knowledge, target **Traditional Chinese free-text administrative ledgers**, Taiwan-specific island flight rules, or map-backed audit trails for Category 6 sub-ledgers in one lightweight desktop workflow. This project fills that operational gap as a **complementary Category 6 activity-data pipeline**, not as a claim of global first inventorship of university carbon software.

# Functionality

| Stage | Behaviour |
|-------|-----------|
| Input | Excel travel records with a destination (and related) column |
| Location recovery | Regex / pattern cleaning + built-in coordinates, aliases, district→city and China city→hub airport tables |
| Domestic road | OSRM driving distance from campus origin; results cached |
| Offshore / international | Geodesic distance via airport pairs (e.g. Songshan / Taoyuan hubs as configured) |
| Mode heuristic | Rule-based assignment from trip type and distance (e.g. long domestic road legs may be treated as rail); **not** ticket-level mode detection |
| Emissions | \(E = \sum_i d_i \times EF_i\) with simplified kg CO₂e/km factors labelled in code as provisional EPA-style defaults; **users must recalibrate against current Taiwan Ministry of Environment (MOENV) organisational factors or other chosen libraries before formal reporting** |
| Audit / export | Folium HTML maps, optional PNG embeds, Excel distance and carbon summary sheets; route and map caches |

Default factors currently shipped for screening (kg CO₂e/km) include illustrative values such as private car/taxi 0.21, domestic flight 0.133, international flight 0.101, rail/HSR 0.034, and bus 0.065. These are **simplified screening coefficients**, not a verified one-to-one binding to any single MOENV gazette table year, and they omit aviation non-CO₂ radiative forcing multipliers [@lee2021]. Great-circle air distances omit detours, holding patterns, and aircraft-type detail; public OSRM endpoints may differ from a self-hosted Taiwan extract. Own fleet fuel belongs in Scope 1, not Category 6.

# Research and administrative use

The pipeline has been exercised on multi-hundred to ~1,000-row annual university travel ledgers in a Fu Jen Catholic University sustainability-reporting setting, producing distance tables, mode-heuristic carbon summaries, and map artefacts for review. Formal gold-standard evaluation of place extraction and distance error (e.g. precision/recall, MAPE against independent mileages) remains future work; release packages should include anonymised example data and version-pinned coordinates.

# Acknowledgements

[PLACEHOLDER: thank sustainability / finance office collaborators; OSRM, OpenStreetMap, Folium, and Geopy communities. Confirm consent for any institutional case description.]

# References
