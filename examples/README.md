# Examples

`sample_travel_records.csv` is a **synthetic, anonymized** mini-ledger for demos and tests.

- No real employee IDs, voucher numbers, or personal names
- Destinations illustrate domestic districts, 台/臺 variants, offshore islands, and international cities

## Quick library check

```bash
cd /path/to/repo
python3 -m pip install -e ".[dev]"
python3 -c "from travel_carbon import calculate_carbon_emission; print(calculate_carbon_emission('國際-飛行', 1000))"
pytest -q
```

## Desktop GUI

```bash
python3 travel_distance_calculator_gui_cached_efficient.py
```

Load a real campus Excel file only on machines that are authorized to process it.
Do **not** commit real reimbursement workbooks.
