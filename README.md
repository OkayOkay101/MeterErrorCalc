# Meter Error Calculator (`MeterErrorCalc`)

[ภาษาไทย](README_TH.md)

Streamlit calculator for meter percentage error comparing before-fix and after-fix three-rate power measurements.

## Requirements

- Python 3
- `streamlit`, `pandas`

## Setup and run

Create a virtual environment, install dependencies, and start the Streamlit app:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install streamlit pandas
streamlit run file.py
```

## How it works

- **Before-fix & After-fix tabs**: Enter Voltage (`V`), Current (`I`), and Power Factor (`PF`) for `Rate A`, `Rate B`, and `Rate C` (blank inputs default to `0.0`).
- **Power calculation**: Computes `kW = (V * I * PF) / 1000` per rate and sums all three rates.
- **Summary tab**: Computes `((total_old / total_new) - 1) * 100` when `total_new > 0` (otherwise `0.0`), flags Fast (`> 0%`), Slow (`< 0%`), or `0%` error, and renders a per-rate comparison table.

## Project layout

| Path | Purpose |
|---|---|
| `file.py` | Streamlit application entry point |
