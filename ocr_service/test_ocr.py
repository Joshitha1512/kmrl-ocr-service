import requests
import json
import os


url = "http://127.0.0.1:5000/upload"
file_path = "samples/bilingual_handwritten.png"  
output_dir = "outputs"                   


os.makedirs(output_dir, exist_ok=True)


with open(file_path, "rb") as f:
    files = {"file": f}
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            extracted_text = response.json().get("extracted_text", "")
            print("Extracted Text:")
            print(extracted_text)

        
            output_file = os.path.join(
                output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}_output.json"
            )
            with open(output_file, "w", encoding="utf-8") as out:
                json.dump({"extracted_text": extracted_text}, out, ensure_ascii=False, indent=4)
            print(f"\nExtracted text saved to {output_file}")

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print("Error connecting to the OCR server:", e)
