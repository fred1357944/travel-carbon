# Emission factor honesty notes

## Defaults shipped in code (`travel_carbon.carbon`)

| Mode (GUI label) | Factor (kg CO₂e/km) | Role |
|------------------|---------------------|------|
| 自用車/計程車 | 0.21 | Default car/taxi |
| 國內航班 | 0.133 | Domestic / island air |
| 國際航班 | 0.101 | International air |
| 火車/高鐵 | 0.034 | Rail / HSR heuristic |
| 巴士 | 0.065 | Bus (available; mode heuristic rarely selects) |

These are **simplified operational defaults** used by the desktop tool. Historical GUI comments referred to “台灣環保署 2023-style” values. **Do not claim full compliance** with Taiwan MOENV statutory tables until each row is reconciled to the official ODS/PDF for the inventory year.

## Official sources to reconcile (before journal/JOSS claims)

1. 環境部事業溫室氣體排放量資訊平台 — **113年2月5日公告溫室氣體排放係數**  
   https://ghgregistry.moenv.gov.tw/epa_ghg/Downloads/FileDownloads.aspx?Type_ID=1
2. 《溫室氣體排放量盤查作業指引》113年版  
3. Optional international benchmarks (comparison only): UK DESNZ conversion factors; ICAO ICEC (aviation CO₂ methodology)

## Mode heuristics (must disclose)

| Rule | Behavior |
|------|----------|
| Label contains `國際` | International flight factor |
| Label contains `離島` or `航班` | Domestic flight factor |
| Label contains `開車` and distance > 300 km | Treat as 火車/高鐵 |
| Label contains `開車` and distance ≤ 300 km | Car/taxi |
| Otherwise by distance | >500 km domestic air; >300 km rail; else car |

These are **not** observed booking modes. Sensitivity analysis is recommended for any institutional total.

## Radiative forcing (RFI)

Default calculations are **without** aviation non-CO₂ / RFI multipliers. GHG Protocol allows RF multipliers only if disclosed. ICAO ICEC is CO₂-oriented. If RFI is applied, report the factor and literature basis separately.

## Suggested Methods wording (English)

> We apply a distance-based approach consistent with GHG Protocol Scope 3 Category 6 guidance: emissions equal distance multiplied by a mode-specific emission factor. Default factors are simplified operational values distributed with the software; users should substitute Taiwan MOENV announced factors (or another chosen database) for formal inventory reporting. Transport mode is inferred from voucher labels and distance heuristics when the ledger does not record mode. Aviation radiative forcing is not included in the default results.
