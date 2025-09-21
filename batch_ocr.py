import os
import json
from pathlib import Path
from PIL import Image
import pytesseract
import pdfplumber
import easyocr

DATASET_PATH = "kmrl_dataset"      
OUTPUT_PATH = "outputs/ocr_dataset.json"
SUBFOLDERS = ["pdf", "png", "noisy", "blur"]
HANDWRITTEN_KEYWORD = "handwritten"  

Path("outputs").mkdir(exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text.strip()

def extract_text_from_image(file_path, handwritten=False):
    try:
        if handwritten:
            reader = easyocr.Reader(['ml', 'en'])
            result = reader.readtext(file_path, detail=0)
            return " ".join(result).strip()
        else:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img, lang="eng+mal").strip()
    except Exception as e:
        print(f"Error reading image {file_path}: {e}")
        return ""

def get_all_files():
    files = []
    for subfolder in SUBFOLDERS:
        folder_path = Path(DATASET_PATH) / subfolder
        if folder_path.exists():
            for file in folder_path.iterdir():
                if file.suffix.lower() in [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
                    files.append(file)
    return files

def main():
    files = get_all_files()
    if not files:
        print("Found 0 files for OCR.")
        return

    print(f"Found {len(files)} files for OCR.")
    ocr_results = {}

    for file in files:
        print(f"Processing: {file.name}")
        handwritten = HANDWRITTEN_KEYWORD in file.stem.lower()
        if file.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(file)
        else:
            text = extract_text_from_image(file, handwritten)

        ocr_results[file.name] = text

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(ocr_results, f, ensure_ascii=False, indent=2)

    print(f"\nOCR completed. Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
