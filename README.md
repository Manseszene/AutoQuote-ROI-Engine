# AutoQuote ROI Engine

AutoQuote ROI Engine standardizes heterogeneous supplier quotations, maps each line item to a user-owned master material code and description, runs volume-based ROI analysis, and generates a concise executive PPT report.

## Target Architecture

The project is organized as three pipeline modules.

1. Data Ingestion & Normalization
   - Parses Excel, text PDF, and scanned image PDF quotations.
   - Uses the master material code-description list as the canonical sorting and matching reference.
   - Uses GPT-4o / GPT-4o-mini to map omitted or supplier-specific descriptions back to the standard code and description.
   - Preserves original currency amounts and calculates KRW converted amounts through user-provided exchange-rate variables.
   - Normalizes supplier-specific cost labels into the six standard cost categories below.

2. Volumetric ROI Analysis Core
   - Uses the normalized final unit cost from the six cost categories.
   - Calculates total cost by expected production volume and compares supplier efficiency across the requested volume range.
   - Stores analysis results as Pandas DataFrames and exports chart images with Matplotlib or Seaborn.

3. Automated Executive PPT Report Generator
   - Generates a one-to-two slide executive PPTX report with `python-pptx`.
   - Slide 1 summarizes supplier quotations by master material code and recommends the best supplier by volume range.
   - Slide 2 visualizes cost curves and break-even points.

## Standard Cost Categories

The normalized quote schema uses these six categories. Their KRW-converted sum is treated as the final calculated unit cost.

```text
1. Material
2. Processing
3. Management/Overhead
4. Local Tax
5. Profit 1
6. Profit 2
```

Notes:

- Korean supplier quotes are assumed to be VAT-exclusive by default, so Local Tax is usually zero or omitted.
- Vietnamese supplier quotes may include local special tax for mold delivery from a Vietnamese tooling supplier to a Vietnamese manufacturer; that amount must be classified as Local Tax.
- Double-margin structures involving subcontractors should use Profit 1 for the main supplier and Profit 2 for the second vendor.

## Initial Directory Tree

```text
autoquote-roi-engine/
|-- .env.example
|-- requirements.txt
|-- README.md
|-- data/
|   |-- input/
|   |   |-- .gitkeep
|   |-- master/
|   |   |-- .gitkeep
|   |-- normalized/
|   |   |-- .gitkeep
|-- docs/
|   |-- .gitkeep
|-- logs/
|   |-- .gitkeep
|-- reports/
|   |-- .gitkeep
|   |-- charts/
|   |   |-- .gitkeep
|-- src/
|   |-- autoquote_roi_engine/
|   |   |-- __init__.py
|   |   |-- config.py
|   |   |-- cli.py
|   |   |-- ingestion/
|   |   |   |-- __init__.py
|   |   |   |-- excel_parser.py
|   |   |   |-- pdf_parser.py
|   |   |   |-- vision_parser.py
|   |   |   |-- normalizer.py
|   |   |-- roi/
|   |   |   |-- __init__.py
|   |   |   |-- analyzer.py
|   |   |   |-- charts.py
|   |   |-- reporting/
|   |   |   |-- __init__.py
|   |   |   |-- ppt_generator.py
|   |   |-- schemas/
|   |   |   |-- __init__.py
|   |   |   |-- quote.py
|   |   |   |-- report.py
|   |   |-- services/
|   |   |   |-- __init__.py
|   |   |   |-- llm_client.py
|   |   |-- utils/
|   |   |   |-- __init__.py
|   |   |   |-- currency.py
|   |   |   |-- logging.py
|-- tests/
|   |-- __init__.py
|   |-- fixtures/
|   |   |-- .gitkeep
|   |-- test_currency.py
|   |-- test_roi_analyzer.py
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

For scanned PDF support on Windows, install Tesseract OCR and Poppler separately, then set `TESSERACT_CMD` and `POPPLER_BIN_PATH` in `.env`.
