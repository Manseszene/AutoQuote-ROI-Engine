# AutoQuote ROI Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![OpenAI Component](https://img.shields.io/badge/OpenAI-Powered-00a37f.svg)](https://openai.com)

AutoQuote ROI Engine standardizes heterogeneous supplier quotations, maps each line item to a user-owned master material code and description, runs volume-based ROI analysis, and generates a concise executive PPT report.

## Problem Statement

In manufacturing, hardware engineering, and procurement teams, reviewing vendor quotes is often manual, error-prone, and slow.

- Quotes arrive in inconsistent formats, including Excel files, text PDFs, and scanned image PDFs.
- Supplier cost labels differ across vendors, regions, currencies, and subcontracting structures.
- Procurement decisions require normalized cost comparison across expected production volumes.

AutoQuote ROI Engine is designed as an end-to-end automation pipeline powered by structured data models, financial analysis logic, and OpenAI-assisted parsing.

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

```text
[Raw Quotes] -> [Parsing & LLM Mapping] -> [Six-Cost Normalization] -> [Volume ROI Analysis] -> [PPTX Report]
```

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
|-- .gitignore
|-- LICENSE
|-- pyproject.toml
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
|   |   |-- roi/
|   |   |-- reporting/
|   |   |-- schemas/
|   |   |   |-- quote.py
|   |   |-- services/
|   |   |-- utils/
|-- tests/
|   |-- fixtures/
|   |-- test_quote_schema.py
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

## Test

```powershell
python -m pytest
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
