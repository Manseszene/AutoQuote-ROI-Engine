# AutoQuote-ROI-Engine
An AI-powered automation tool to parse unstructured vendor quotes, calculate ROI, and generate structured executive reports.
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
