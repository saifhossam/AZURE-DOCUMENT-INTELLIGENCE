# 📄 Document Intelligence App

A Streamlit web application for extracting and analyzing structured data from documents using **Azure Document Intelligence** (formerly Form Recognizer). Upload a PDF or image and get back JSON, tables, key-value pairs, and model-specific fields — all in a clean, tabbed UI.

---

## Features

- **Multiple prebuilt models** — OCR, Layout, General Document, Invoice, and Receipt
- **Structured JSON output** — clean, export-ready results saved to disk automatically
- **Tabbed results UI** — view extracted fields, tables, key-value pairs, and raw text side-by-side
- **Invoice & Receipt enhancers** — dedicated field extraction (vendor, customer, line items, totals)
- **Download support** — grab the full JSON or raw text directly from the UI
- **Live Azure status** — sidebar shows whether credentials are configured

---

## Screenshots

> Upload & Analyze → Results tabs (JSON · Tables · Key-Value Pairs · Extracted Fields · Raw Text)

---

## Project Structure

```
.
├── app.py               # Streamlit entry point
├── analyzer.py          # Single analysis pipeline (validate → Azure → parse → enhance → save)
├── azure_client.py      # Azure SDK wrapper & result serialization
├── config.py            # All settings (Azure credentials, file limits, output dir)
├── display.py           # Streamlit result rendering (tabs, metrics, downloads)
├── enhancers.py         # Invoice & Receipt field enhancers
├── file_handler.py      # File validation and JSON output saving
├── json_parser.py       # Transforms raw Azure result into clean export dict
├── layout.py            # Page config, sidebar, and shared UI components
├── registry.py          # Single source of truth for all model definitions
└── table_parser.py      # Converts parsed JSON into pandas DataFrames
```

---

## Supported Models

| Display Name       | Azure Model ID       | Enhanced Extraction |
|--------------------|----------------------|---------------------|
| OCR (Read)         | `prebuilt-read`      | —                   |
| Layout Analyzer    | `prebuilt-layout`    | —                   |
| General Document   | `prebuilt-document`  | —                   |
| Invoice            | `prebuilt-invoice`   | ✅ Yes              |
| Receipt            | `prebuilt-receipt`   | ✅ Yes              |

---

## Getting Started

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

<details>
<summary>Core dependencies</summary>

```
streamlit
azure-ai-formrecognizer
azure-core
pandas
python-dotenv
```

</details>

### 3. Configure Azure credentials

Create a `.env` file in the project root:

```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=<your-api-key>

# Optional
OUTPUT_DIR=outputs
```

> **Finding your credentials:** In the Azure Portal, go to your Document Intelligence resource → **Keys and Endpoint**.

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Usage

1. **Select a model** in the sidebar (default: General Document)
2. **Upload a file** — PDF, PNG, JPG, JPEG, TIFF, or BMP, up to 50 MB
3. Click **🚀 Analyze Document**
4. Explore results across five tabs:
   - **JSON** — full structured output with download button
   - **Tables** — any detected tables rendered as DataFrames
   - **Key-Value Pairs** — key-value pairs with confidence scores
   - **Extracted Fields** — model-specific fields (e.g. InvoiceTotal, MerchantName)
   - **Raw Text** — all document text with line count and download button
5. Results are also auto-saved to `outputs/json/` as timestamped JSON files

---

## Output Format

Every analysis returns a structured JSON object:

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
    "total_kv_pairs": 8,
    "total_fields": 12,
    "total_words": 340
  },
  "pages": [...],
  "tables": [...],
  "key_value_pairs": [...],
  "extracted_fields": {...},
  "raw_text": "...",
  "invoice_details": {...}   // Invoice model only
}
```

---

## Adding a New Model

All models are defined in `registry.py`. To add a new one:

```python
"My Custom Model": ModelDefinition(
    model_id="prebuilt-<model-id>",
    display_name="My Custom Model",
    description="What this model does.",
    has_enhancer=False,
)
```

If the model needs custom field extraction, add a handler in `enhancers.py` and set `has_enhancer=True`.

---

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` | *(required)* | Azure resource endpoint URL |
| `AZURE_DOCUMENT_INTELLIGENCE_KEY` | *(required)* | Azure API key |
| `OUTPUT_DIR` | `outputs` | Directory for saved JSON results |

File limits are set in `config.py`:

```python
SUPPORTED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
MAX_FILE_SIZE_MB = 50
```
MIT
