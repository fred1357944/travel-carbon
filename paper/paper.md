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

Higher-education institutions (HEIs) increasingly report greenhouse-gas (GHG) inventories that include employee business travel under the GHG Protocol Corporate Value Chain (Scope 3) Standard, Category 6 (*Business travel*) [@ghgprotocol_cat6]. When activity data are incomplete, organisations often rely on spend-based estimates. Distance-based methods improve data quality when trip distances and modes can be recovered, but many Taiwanese campuses store evidence as **administrative Excel ledgers with free-text Traditional Chinese destinations**, not structured travel-management feeds.

`travel-carbon` is an open-source Python package and desktop workflow that (i) normalises free-text destinations using a rule- and gazetteer-based pipeline (台/臺 variants, district→city and city→airport maps); (ii) estimates distances with a Taiwan-oriented hybrid policy—optional OSRM road routing for mainland driving from a campus origin (default: Fu Jen Catholic University) and geodesic distances for offshore-island and international air legs [@huber2016; @osrm]; (iii) multiplies distances by transparent **screening** emission factors in the style of GHG Protocol Category 6 distance-based accounting; and (iv) supports Folium route maps in the GUI as visual audit trails. A library API (`estimate_trip`), CLI (`python -m travel_carbon`), and offline evaluation harness are included for reproducible checks without personal data.

The software is aimed at HEI sustainability and finance staff and at researchers who need an inspectable Category 6 **sub-pipeline**. It complements multi-scope campus tools rather than replacing full organisational inventories.

# Statement of need

Academic and administrative travel can be a material share of campus climate inventories [@ciers2019; @vallsval2021; @kiehle2023]. Taiwanese HEIs are also expanding ISO 14064-style organisational accounting that includes business travel [@tsai2025]. In practice, Category 6 quality is limited by **data form**: free-text reimbursement rows rather than machine-readable itineraries. Manual map look-ups are slow and hard to audit.

Open tools such as the campus estimator of @auger2021, **CO2UNV** [@vallsval2022], and **GES 1point5** [@mariette2022] serve important laboratory- and multi-scope use cases, typically with structured activity inputs. They do not target **Traditional Chinese free-text administrative ledgers**, Taiwan island flight rules, and map-backed Category 6 audit trails in one lightweight desktop package. `travel-carbon` addresses that operational gap as a **complementary** pipeline—not a claim of global first inventorship of university carbon software.

# Functionality

| Component | Behaviour |
|-----------|-----------|
| `travel_carbon.data` | Built-in gazetteer (coordinates, aliases, district and hub mappings) |
| `travel_carbon.locations` | Free-text normalisation and mainland / island / international classification |
| `travel_carbon.distance` | OSRM driving (optional network) or geodesic×1.4 fallback; island and international geodesic flights |
| `travel_carbon.carbon` | Mode heuristics; factor profiles `screening` and `taiwan_cfp` from YAML |
| `travel_carbon.pipeline` | `estimate_trip()` end-to-end helper |
| Desktop GUI | Batch Excel ingest, caches, Folium maps, carbon summary export |
| Eval harness | Offline gold CSV scoring (`python -m travel_carbon.eval_batch`) |

Default **screening** factors (kg CO₂e/km) are operational values shipped for demos (e.g. car/taxi 0.21, domestic air 0.133, international air 0.101, rail/HSR 0.034, bus 0.065). They are **not** a line-item mapping to Taiwan MOENV’s organisation fuel-factor gazette (kg/TJ). Among screening values, HSR 0.034 aligns with a published product-CFP high-speed-rail entry; the `taiwan_cfp` profile lowers private-car factors toward product-CFP pkm values for sensitivity analysis. Users must recalibrate for formal ISO 14064-1 reporting. Aviation non-CO₂ radiative forcing is omitted by default [@lee2021].

# Quality assurance

Unit tests cover carbon arithmetic, gazetteer resolution, offline distances, factor loading, and the evaluation harness (48 tests at v0.1). A **synthetic** gold set (`examples/sample_travel_gold_50.csv`, *n* = 52) exercises mainland districts, 台/臺 variants, offshore islands, international hubs, and empty destinations. Offline evaluation reports kind accuracy 1.0 and mode-heuristic accuracy 1.0 on that set (geodesic fallback; no public OSRM required). This is **not** a substitute for labelled extraction precision/recall or MAPE against independent mileages on real institutional ledgers, which remain recommended future work. Real reimbursement workbooks are excluded from version control.

# Acknowledgements

We thank the OpenStreetMap, OSRM, Folium, and Geopy communities. Institutional case use of annual travel ledgers at Fu Jen Catholic University motivated the workflow; only synthetic examples are distributed in the public tree.

# References
