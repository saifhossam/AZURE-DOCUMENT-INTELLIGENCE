# Document Intelligence App - 5 Models

A Streamlit-based document analysis application powered by Azure Document Intelligence, supporting 5 pre-built models for OCR, layout analysis, and data extraction from invoices, receipts, and general documents.

---

## 📋 Project Overview

This application provides an intuitive UI for document analysis using Azure's Document Intelligence service. Users can upload documents (PDF, PNG, JPG, TIFF, BMP), select from 5 analysis models, and receive structured extracted data with optional Excel export.

---

## 🔄 Data Pipeline Overview

```
User Upload → Validation → Model Resolution → Azure Analysis → Parsing → Output Storage → Display
   (main.py)  (file_handler)  (model_router)  (document_service) (json_parser) (file_handler) (display.py)
```

### Pipeline Flow:

1. **User Upload** (`main.py` + `ui/layout.py`)
   - Web UI accepts documents via Streamlit file uploader
   - Supported formats configured in `utils/config.py`

2. **File Validation** (`utils/file_handler.py`)
   - Validates file type and size
   - Converts file to bytes for Azure submission

3. **Model Resolution** (`services/model_router.py`)
   - Maps user-friendly model names to Azure model IDs
   - Factory pattern via `models/model_factory.py`

4. **Azure Analysis** (`services/document_service.py`)
   - Authenticates with Azure using credentials from `.env`
   - Sends file bytes to Azure Document Intelligence API
   - Returns raw structured result with pages, tables, key-value pairs

5. **Result Parsing** (`parsers/json_parser.py`)
   - Transforms raw Azure output into clean, exportable JSON
   - Extracts metadata, pages, tables, fields, and confidence scores

6. **Output Storage** (`utils/file_handler.py`)
   - Saves parsed JSON to `outputs/json/`
   - Optionally saves tables to `outputs/tables/`

7. **Display & Export** (`ui/display.py` + `ui/layout.py`)
   - Renders results in Streamlit tabs
   - Enables Excel export for downstream analysis

---

## 📁 Directory Structure & File Purposes

### Root Level

| File | Purpose |
|------|---------|
| `main.py` | **Entry point** – Streamlit app orchestrator; initializes UI, handles session state, ties together layout and inference |
| `requirements.txt` | Python dependencies (Streamlit, Azure SDK, Pandas, etc.) |

### `/controllers/`
Orchestrates the inference workflow end-to-end.

| File | Purpose |
|------|---------|
| `inference_controller.py` | **Workflow orchestrator** – Manages the full pipeline: validates → resolves model → calls Azure → parses → saves → returns result |

### `/models/`
Model definitions and factory pattern for managing 5 pre-built Azure models.

| File | Purpose |
|------|---------|
| `base_model.py` | Abstract base class defining model interface (name, description, config) |
| `model_factory.py` | **Factory pattern** – Registry mapping display names to model classes; creates model instances |
| `ocr_model.py` | OCR (Read) model: basic text extraction |
| `layout_model.py` | Layout Analysis model: text, regions, page structure |
| `general_doc_model.py` | General Document model: key-value pairs, tables, entities |
| `invoice_model.py` | Invoice model: extracts invoice-specific fields (amount, date, vendor, etc.) |
| `receipt_model.py` | Receipt model: extracts receipt-specific fields (line items, total, merchant, etc.) |

### `/services/`
Core business logic for API communication and routing.

| File | Purpose |
|------|---------|
| `document_service.py` | **Azure client** – Authenticates, submits documents to Azure Document Intelligence API, deserializes responses |
| `model_router.py` | **Router** – Maps user-selected model names to Azure model IDs; uses `model_factory.py` |

### `/ui/`
Frontend rendering logic for Streamlit.

| File | Purpose |
|------|---------|
| `layout.py` | **Page layout** – Configures page settings, sidebar, header, metrics, metadata sections; applies custom CSS |
| `display.py` | **Results display** – Renders tabbed results view, error/success messages, pages summary |

### `/parsers/`
Transform raw Azure output into clean, structured formats.

| File | Purpose |
|------|---------|
| `json_parser.py` | **JSON transformer** – Converts raw Azure result dict into export-ready JSON with metadata, summary, pages, tables, fields, text |
| `table_parser.py` | **Table extractor** – Parses table data from Azure result; optional dedicated table extraction |

### `/utils/`
Utility functions for configuration and file handling.

| File | Purpose |
|------|---------|
| `config.py` | **Configuration** – Loads Azure credentials from `.env`; defines app constants (supported file types, paths, etc.) |
| `file_handler.py` | **File I/O** – Validates file type/size, saves JSON output to disk, manages file paths |

### `/outputs/`
Output storage directories.

| Directory | Purpose |
|-----------|---------|
| `outputs/json/` | Stores parsed JSON results (one per document analysis) |
| `outputs/tables/` | Optional: stores extracted tables in separate format |

---

## 🔌 Component Interaction Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         main.py (Streamlit App)                       │
│  └─ initialize_session_state()                                        │
│  └─ page_upload_analyze()                                             │
│     └─ calls: inference_controller.run_inference()                    │
└──────────────────────────────────────────────────────────────────────┘
                                 ↓
┌──────────────────────────────────────────────────────────────────────┐
│              inference_controller.py (Pipeline Orchestrator)           │
│  1. file_handler.validate_file()                                      │
│  2. model_router.resolve_model_id()                                   │
│  3. document_service.analyze_document()                               │
│  4. json_parser.build_json_output()                                   │
│  5. file_handler.save_json_output()                                   │
└──────────────────────────────────────────────────────────────────────┘
           ↓                           ↓                    ↓
    ┌────────────┐            ┌──────────────┐    ┌────────────────┐
    │model_router│            │document_     │    │file_handler &  │
    │            │            │service.py    │    │json_parser.py  │
    │Resolves:   │            │              │    │                │
    │OCR→        │            │Calls Azure   │    │Transform & Save│
    │Layout→     │ ────────→  │API with file │    │to outputs/json/│
    │General→    │            │bytes & model │    │                │
    │Invoice→    │            │ID            │    │                │
    │Receipt     │            │              │    │                │
    └────────────┘            └──────────────┘    └────────────────┘
           ↑                           ↑                    ↓
    model_factory.py                Azure SDK        ┌────────────┐
    (DISPLAY_NAME_MAP)             FormRecognizer    │display.py  │
                                                     │ render tabs│
                                                     │ show results
                                                     └────────────┘
```

---

## 🛠️ How to Run

### Prerequisites
- Python 3.8+
- Azure Document Intelligence credentials (set in `.env`)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with Azure credentials
# AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=<your-endpoint>
# AZURE_DOCUMENT_INTELLIGENCE_KEY=<your-key>

# Run the Streamlit app
streamlit run main.py
```

### Usage

1. **Upload Document**: Choose a supported file format (PDF, PNG, JPG, TIFF, BMP)
2. **Select Model**: Choose from 5 models (OCR, Layout, General, Invoice, Receipt)
3. **Analyze**: Submit for analysis via Azure Document Intelligence
4. **View Results**: Inspect extracted data in tabs (Pages, Tables, Fields, Key-Value Pairs, Raw Text)
5. **Export**: Save results as Excel or JSON

---

## 📦 Key Dependencies (requirements.txt)

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `azure-ai-formrecognizer` | Azure Document Intelligence SDK |
| `azure-core` | Azure authentication |
| `python-dotenv` | Load `.env` credentials |
| `pandas` | Data manipulation and Excel export |
| `Pillow` | Image handling |
| `openpyxl` | Excel file generation |
| `plotly` | Optional visualization |

---

## 🧠 Model Details

| Model | Azure ID | Use Case |
|-------|----------|----------|
| **OCR (Read)** | `prebuilt-read` | Basic text extraction from any document |
| **Layout** | `prebuilt-layout` | Extract text, regions, table structure, reading order |
| **General Document** | `prebuilt-document` | Key-value pairs, tables, entities from generic docs |
| **Invoice** | `prebuilt-invoice` | Invoice-specific fields: amount, date, vendor, items |
| **Receipt** | `prebuilt-receipt` | Receipt-specific fields: items, total, merchant, date |

---

## 📊 Output Structure (JSON Example)

```json
{
  "meta": {
    "filename": "invoice.pdf",
    "model": "Invoice",
    "azure_model_id": "prebuilt-invoice",
    "analyzed_at": "2026-04-09T14:30:00"
  },
  "summary": {
    "pages": 1,
    "tables": 1,
    "fields_extracted": 12,
    "key_value_pairs": 8
  },
  "pages": [
    {
      "page_number": 1,
      "dimensions": "8.5 x 11 in",
      "line_count": 25,
      "word_count": 120,
      "lines": ["Invoice Date: 2026-04-09", "..."]
    }
  ],
  "tables": [
    {
      "table_index": 0,
      "rows": [["Item", "Quantity", "Price"], ["..."]
    }
  ],
  "key_value_pairs": [
    {
      "key": "Invoice ID",
      "value": "INV-12345",
      "confidence": 0.95
    }
  ],
  "extracted_fields": {
    "InvoiceDate": {
      "value": "2026-04-09",
      "confidence": 0.98
    }
  },
  "raw_text": "Full concatenated text from all pages..."
}
```

---

## 🔐 Security Notes

- **Credentials**: Store Azure credentials in `.env` (never commit to version control)
- **File Handling**: Uploaded files are processed in memory; local temp files are cleaned up
- **Output**: Saved JSON files stored locally in `outputs/json/`
