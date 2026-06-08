# AutoQuote-ROI-Engine 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![OpenAI Component](https://img.shields.io/badge/OpenAI-Powered-00a37f.svg)](https://openai.com)

An enterprise-grade open-source automation framework designed to parse highly unstructured vendor quotes, standardize global pricing items, calculate financial Return on Investment (ROI), and automatically generate executive-ready reports using LLMs.

---

## 📌 Problem Statement

In manufacturing, hardware engineering, and procurement industries, reviewing vendor quotes is a highly manual, error-prone, and time-consuming process.

- **Unstructured Data:** Quotes arrive in disparate formats (multi-page PDFs, complex Excel sheets, localized formats).
- **Inconsistent Cost Structures:** Comparing different vendors requires tedious manual normalization of unit prices, tooling costs, and setup fees.
- **Delayed Decision Making:** Calculating financial metrics like ROI, Net Present Value (NPV), and Payback Periods manually delays crucial project approvals.

**AutoQuote-ROI-Engine** solves this by creating an automated end-to-end data pipeline driven by Advanced Language Models.

---

## 🏗️ System Architecture & Data Flow

```text
[ Raw Input ]       ->   [ Parsing Engine ]    ->   [ Analysis Core ]      ->   [ Output Layer ]
- Vendor PDFs            - LLM Table Extraction     - Cost Normalization        - Markdown Summary
- Excel Quotations       - Text Standardization     - ROI / NPV Logic Engine    - Executive PDF Report
- Email Price Lists      - JSON Schema Validation   - Cross-Vendor Comparison   - ERP-Ready CSV
```

---

## ✨ Key Features

### 1. Intelligent Multi-Modal Parsing
Utilizes advanced LLM capabilities to intelligently recognize and extract nested pricing tables, localized currency data, hidden manufacturing setup fees, and handwritten engineering notes from diverse document templates.

### 2. Advanced Financial Intelligence Engine
Automates complex financial evaluations based on customizable corporate business logic:
- **ROI Calculation:** Automated formulas assessing net benefits against total initial investment costs.
- **Payback Period Analysis:** Predicts break-even timelines across multi-vendor scenarios.
- **Incoterms & Tax Normalization:** Automatically adjusts comparison metrics based on shipping terms (EXW, FOB, DDP) and duties.

### 3. Automated Executive Report Generator
Translates raw financial and technical metrics into professional, natural-language business insights, outputting a standardized executive summary report in Markdown and PDF formats.

---

## 🗺️ Project Roadmap & OpenAI Grant Vision

This project is scaling rapidly, and support from the OpenAI OSS Program will accelerate our capabilities:

- **Phase 1 (Current):** Basic rule-based parsing and static JSON cost structuring for single-page text-based PDFs.
- **Phase 2 (Target with OpenAI Credits):**
  - Integrate **GPT-4o Multi-modal Vision API** to accurately interpret blueprints, hardware layout diagrams, and complex multi-page nested tables embedded in vendor quotes.
  - Implement dynamic prompt engineering to minimize data hallucination rates under 0.1%.
- **Phase 3 (Future Expansion):** Deploy an autonomous agent workflow capable of drafting automated counter-proposal emails to vendors based on the generated ROI analysis.

---

## 🛠️ Tech Stack

- **Core:** Python 3.10+
- **AI/LLM:** OpenAI API (GPT / Codex)
- **Data Pipeline:** Pandas, Pydantic (Data validation & JSON schema enforcement)
- **Document Processing:** PyPDF, OpenPyXL

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Manseszene/AutoQuote-ROI-Engine.git
cd AutoQuote-ROI-Engine
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory and add your credentials (do not commit this file to GitHub):

```env
OPENAI_API_KEY=your_openai_api_key_here
COMPANY_ROI_THRESHOLD=0.15
```

### Usage

```bash
python main.py --input ./sample_quotes/vendor_a.pdf
```

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please read our contributing guidelines before submitting a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
