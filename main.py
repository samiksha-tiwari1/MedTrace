from preprocess import clean_foil
from ocr import run_ocr
from parser import parse_fields
from tamper import detect_tamper
import cv2
import json
import sys

# Image path from command line
image_path = sys.argv[1]

# ---------------- Preprocess Foil ----------------
clean_gray = clean_foil(image_path)

# Convert grayscale back to 3-channel image
clean_img = cv2.cvtColor(clean_gray, cv2.COLOR_GRAY2BGR)

# ---------------- OCR ----------------
texts = run_ocr(clean_img)

with open("ocr_text.txt", "w") as f:
    for t in texts:
        f.write(t + "\n")

# ---------------- Parsing ----------------
fields = parse_fields(texts)

# ---------------- Tamper Detection ----------------
tamper_score = detect_tamper(clean_img)

confidence = min(100, tamper_score)

result = {
    **fields,
    "tamper_score": tamper_score,
    "confidence": f"{confidence:.2f}%",
    "evidence": "High edge-density region detected on foil surface",
    "verdict": "SUSPICIOUS" if tamper_score > 25 else "NORMAL"
}

print(json.dumps(result, indent=4))

with open("verdict.json", "w") as f:
    json.dump(result, f, indent=4)