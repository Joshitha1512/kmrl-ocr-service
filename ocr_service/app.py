from flask import Flask, request, jsonify
import pdfplumber
import pytesseract
from PIL import Image
import os

app = Flask(__name__)


pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Joshitha Mugunthan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

@app.route("/")
def home():
    return "OCR backend is running! Use POST /upload with a file."


@app.route("/upload", methods=["POST"])
@app.route("/upload/", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

  
    filename = file.filename
    file.save(filename)

    text = ""
    try:
        if filename.lower().endswith(".pdf"):
            with pdfplumber.open(filename) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img = Image.open(filename)
            text = pytesseract.image_to_string(img, lang="eng+mal")
        else:
            return jsonify({"error": "Unsupported file format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
       
        if os.path.exists(filename):
            os.remove(filename)

    return jsonify({"extracted_text": text})


if __name__ == "__main__":
   
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
