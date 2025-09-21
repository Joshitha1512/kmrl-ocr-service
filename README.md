# Document Ingestion and OCR – KMRL Project Phase

## Overview

This module handles **document ingestion** and **OCR-based text extraction** from PDFs and images.
It forms the first phase of the Document Overload solution for KMRL, and will later be integrated with summarization, routing, and compliance phases.

Supported features:

* Text extraction from PDFs and images (English + Malayalam)
* Flask API to upload and process documents
* Test client script (`test_ocr.py`) to send files for OCR
* Outputs returned as JSON (and optionally saved locally)

## Directory Structure

kmrl-ocr-service/
│
├── venv/                     ← Python virtual environment
├── ocr_service/              
│   ├── app.py                ← Flask API for OCR
│   └── test_ocr.py           ← Client script to send files
├── samples/                  ← Test documents (PDFs, images)
├── outputs/                  ← (Optional) extracted text JSON files
├── requirements.txt          ← Project dependencies
├── README.md
└── .gitignore


## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

**requirements.txt**:

```
Flask==2.3.6
pytesseract==0.3.12
pdfplumber==0.9.0
Pillow==10.0.1
opencv-python-headless==4.12.0.88
numpy<1.27
requests==2.32.5
```
Ensure Tesseract OCR is installed on your system and added to PATH.


## Running the OCR Server

Activate your virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Run the Flask server:

```bash
python ocr_service\app.py
```

Server will run on: `http://127.0.0.1:5000`


## Testing OCR

Use `test_ocr.py` to send a file to the server:

```bash
python ocr_service\test_ocr.py
```

The script will print the extracted text in the terminal.

**Example Output**:

```json
{
    "extracted_text": "കരേളം തക്കുപടിഞ്ഞാറന്‍ ഒലബോര്‍ തിരദശേ സംസ"
}
```

Optional: Text can also be saved to a JSON file (script writes `outputs/<filename>.json`).

---

## Datasets

Place your test PDFs and images in the `samples/` folder.

**Examples**:

* `bilingual_sample.pdf` → English + Malayalam PDF
* `bilingual_clean.png` → Clean image for OCR
* `bilingual_scanned.png` → Noisy/scanned document





