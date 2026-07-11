# Emission factor honesty notes

## Defaults shipped in code (`travel_carbon.carbon`)

| Mode (GUI label) | Factor (kg CO₂e/km) | vs Taiwan official (honest) |
|------------------|---------------------|-----------------------------|
| 自用車/計程車 | 0.21 | **No match.** CFP 自用小客車 0.115 / 營業小客車 0.133 pkm (2014). Project is higher. |
| 國內航班 | 0.133 | **No generic MOENV match.** Numerically equals 營業小客車, not aviation. Route example 松山–金門 CFP 0.281 (2018). |
| 國際航班 | 0.101 | **No MOENV generic pkm factor.** Use ICAO / foreign libraries; disclose RFI separately. |
| 火車/高鐵 | 0.034 | **Partial match** to 高鐵 CFP 2018 (0.034). Over-simplifies 臺鐵 (higher). |
| 巴士 | 0.065 | **Approx** mid of CFP bus/coach band ~0.044–0.094. |

These are **simplified operational screening defaults**.  
Historical GUI comments (“環保署 2023”) are **overclaims** relative to both:

1. **環境部 113-02-05 公告溫室氣體排放係數** — fuel combustion **kg/TJ** for organizational inventory, **not** passenger-km.  
   https://ghgregistry.moenv.gov.tw/upload/Tools/AI/113年2月5日公告溫室氣體排放係數.pdf  
2. **產品碳足跡資訊網 / CFP_P_02** — the real source class for Taiwan **pkm** service factors.

## Mode heuristics (must disclose)

| Rule | Behavior |
|------|----------|
| Label contains `國際` | International flight factor |
| Label contains `離島` or `航班` | Domestic flight factor |
| Label contains `開車` and distance > 300 km | Treat as 火車/高鐵 |
| Label contains `開車` and distance ≤ 300 km | Car/taxi |
| Otherwise by distance | >500 km domestic air; >300 km rail; else car |

Not observed booking modes. Run sensitivity for institutional totals.

## Radiative forcing (RFI)

Defaults are **without** aviation non-CO₂ / RFI. Disclose if applied.

## Suggested Methods wording

> We apply a distance-based approach consistent with GHG Protocol Scope 3 Category 6: emissions ≈ distance × mode factor. Shipped factors are **screening defaults**, not a line-item mapping to MOENV’s 5 Feb 2024 fuel-factor gazette (kg/TJ). Among defaults, only HSR 0.034 aligns with the 2018 product-CFP high-speed-rail entry; car and aviation defaults should be recalibrated (CFP car 0.115/0.133; aviation via ICAO or route-specific CFP) before formal ISO 14064-1 reporting.

## Recommended sensitivity set (Taiwan-facing)

| Mode | Factor | Source |
|------|--------|--------|
| 自用小客車 | 0.115 kg/pkm | CFP_P_02 2014 |
| 營業小客車/計程車 | 0.133 kg/pkm | CFP_P_02 2014 |
| 高鐵 | 0.034 kg/pkm | CFP_P_02 2018 |
| 巴士/客運 band | 0.044–0.094 kg/pkm | CFP_P_02 |
| 國內航空 (example) | 0.281 kg/pkm 松山–金門 | CFP_P_02 2018 (route-specific) |

Machine-readable draft: `data/factors.yaml`.
