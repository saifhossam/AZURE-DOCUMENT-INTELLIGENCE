# 📄 AZURE Document Intelligence App

A Streamlit web application for extracting and analyzing structured data from documents using **Azure Document Intelligence**.

---

## ✨ Features

- **Multiple Azure prebuilt models** — OCR, Layout, General Document, Invoice, Receipt
- **Structured JSON output** — Clean, exportable results with metadata, pages, tables, and fields
- **Interactive Streamlit UI** — Upload documents, view results across tabbed panels
- **Table extraction** — Detected tables rendered as DataFrames
- **Key-value pair extraction** — Ideal for forms and general documents
- **Field-level extraction** — Invoice/receipt-specific fields with confidence scores
- **Raw text view** — Full concatenated text from all pages
- **JSON download** — Export results directly from the browser
- **File validation** — Format and size checks before sending to Azure

---

## 🏗️ Project Structure

```
├── controllers/
│   └── inference_controller.py   # Orchestrates the full upload → Azure → parse → output pipeline
├── models/
│   ├── base_model.py             # Abstract base class for all document models
│   ├── ocr_model.py              # OCR / Read model
│   ├── layout_model.py           # Layout analysis model
│   ├── general_doc_model.py      # General document model
│   ├── invoice_model.py          # Invoice extraction model
│   ├── receipt_model.py          # Receipt extraction model
│   └── model_factory.py          # Factory for creating model instances
├── parsers/
│   ├── json_parser.py            # Transforms raw Azure results into clean JSON
│   └── table_parser.py           # Converts parsed output into pandas DataFrames
├── services/
│   ├── document_service.py       # Azure Document Intelligence client & serialization
│   └── model_router.py           # Maps display names → Azure model IDs
├── ui/
│   ├── display.py                # Result rendering (tabs, tables, JSON, text)
│   └── layout.py                 # Page config, sidebar, header, metrics
├── utils/
│   ├── config.py                 # Azure credentials and app settings
│   └── file_handler.py           # File validation, saving, and I/O helpers
├── main.py                       # Streamlit app entry point
├── requirements.txt
└── .env                          # Your Azure credentials (not committed)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [Azure Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence) resource (free tier available)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/document-intelligence-app.git
cd document-intelligence-app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Azure credentials

Create a `.env` file in the project root:

```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_api_key_here
APP_ENV=development
OUTPUT_DIR=outputs
```

> You can find your endpoint and key in the **Azure Portal** under your Document Intelligence resource → **Keys and Endpoint**.

### 4. Run the app

```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`.

---

## 🧠 Supported Models

| Display Name      | Azure Model ID       | Best For                                      |
|-------------------|----------------------|-----------------------------------------------|
| OCR (Read)        | `prebuilt-read`      | Scanned documents, images, raw text extraction |
| Layout Analyzer   | `prebuilt-layout`    | Text, tables, and document structure           |
| General Document  | `prebuilt-document`  | Mixed document types, key-value pairs          |
| Invoice           | `prebuilt-invoice`   | Invoices, billing records, vendor/customer info|
| Receipt           | `prebuilt-receipt`   | Receipts, transaction records, line items      |

---

## 📂 Supported File Formats

| Format | Extensions              |
|--------|-------------------------|
| PDF    | `.pdf`                  |
| Images | `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp` |

**Maximum file size:** 50 MB

---

## 📊 Output Structure

Every analysis produces a structured JSON output:

```json
{
  "meta": {
    "filename": "invoice.pdf",
    "model": "Invoice",
    "azure_model_id": "prebuilt-invoice",
    "analyzed_at": "2024-01-15T10:30:00"
  },
  "summary": {
    "total_pages": 1,
    "total_tables": 2,
    "total_key_value_pairs": 5,
    "total_extracted_fields": 12,
    "total_words": 342
  },
  "pages": [ ... ],
  "tables": [ ... ],
  "key_value_pairs": [ ... ],
  "extracted_fields": { ... },
  "raw_text": "..."
}
```

Results are also saved to `outputs/json/` with a timestamped filename.

---

## 🖥️ App Pages

- **Upload & Analyze** — Upload a document, select a model, and run analysis
- **View Results** — Revisit the last analysis result across tabbed views:
  - 📋 Full JSON viewer with download
  - 📊 Extracted tables as DataFrames
  - 🔑 Key-value pairs
  - 📄 Extracted fields with confidence scores
  - 📝 Raw text with download
- **Model Info** — Description and tips for each supported model

---

## 🔧 Configuration

All settings live in `utils/config.py`:

```python
class AppConfig:
    OUTPUT_DIR = "outputs"           # Where JSON results are saved
    MAX_FILE_SIZE_MB = 50            # Upload size limit
    SUPPORTED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
    MODEL_MAP = {                    # Display name → Azure model ID
        "Layout Analyzer": "prebuilt-layout",
        "OCR (Read)": "prebuilt-read",
        ...
    }
```
