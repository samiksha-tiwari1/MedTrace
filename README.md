## MedTrace — Forensic Inspection of Medicine Strip Authenticity

This project focuses on the challenges of computer vision on reflective pharmaceutical packaging — a problem rarely addressed in typical OCR systems.


## 🔬 MedTrace Inspection Demo

![MedTrace Demo](assets/medtrace_demo.gif)
![MedTrace Demo](assets/camera_capture.png)


MedTrace is a forensic computer vision pipeline designed to inspect medicine strip images for signs of tampering, surface disturbance, and authenticity risks.

It combines:
	•	Illumination correction for reflective foil
	•	OCR extraction of printed drug data
	•	Micro-texture forensics using Edge Density + LBP
	•	Evidence-based inspection verdict in structured JSON

Built as a research-grade CV inspection system, not a UI app or demo script.

⸻

🔍 Problem Statement

Critical information like drug name, batch number, and expiry date is printed on reflective aluminum foil.

This surface is:
	•	Prone to scratches and abrasions
	•	Vulnerable to overwriting and tampering
	•		Extremely difficult for OCR due to glare and texture noise
	•	Structurally deformable when pills are pressed and resealed


MedTrace demonstrates how computer vision and surface forensics can be used to detect these anomalies from a simple image.

⸻

 Pipeline Architecture

Input Strip Image
        ↓
Foil Illumination Correction (CLAHE + Bilateral + Morphology)
        ↓
Deskew & Preprocessing
        ↓
OCR Detection (EasyOCR)
        ↓
Texture Forensics
   ├─ Edge Density (Canny)
   └─ LBP Micro-Texture Analysis
        ↓
Anomaly Scoring (0–100)
        ↓
Forensic Inspection Report (JSON)


⸻

 Visual Evidence

## 🧼 Foil Cleaning — 

![Foil Clean](assets/foil_clean.jpg)
Removes glare and foil noise for reliable analysis.


⸻

## OCR Detection — 

![OCR Output](assets/ocr_output.jpg)
Bounding boxes around detected text after preprocessing.


⸻

## Texture Heatmap — 

![Heatmap](assets/tamper_heatmap.jpg)
Edge heatmap showing foil disturbance regions.


⸻

 ## Tamper Region — 

![Tamper Output](assets/tamper_output.jpg)
Most suspicious region highlighted.


⸻

 Techniques Used

Technique	                          Purpose
CLAHE Contrast Normalization	    Remove foil illumination bias
Bilateral Filtering.            	Reduce glare while preserving edges
Morphological Operations	        Remove foil speckles
Deskewing	                        Improve OCR alignment
EasyOCR	                            Text extraction from processed foil
Canny Edge Detection	            Detect scratches / overprints
Local Binary Patterns (LBP)      	Detect micro-texture disturbance
Normalized Multi-Signal             Realistic forensic tamper score


⸻

Observed Performance (Empirical)

These values are from testing on multiple strip images:
	•	Drug name detection: Consistently detected on clear images
	•	OCR reliability on large text: High
	•	OCR reliability on micro-print (batch/expiry): Limited by camera resolution and foil reflectivity
	•	Tamper region localization: Visually consistent across samples
	• Blister cavity deformation detection: Clearly highlights irregular cavities
	•	Processing time per image: ~1.2–2.0 seconds

MedTrace intentionally reports when micro-print OCR is unreliable — mimicking real inspection systems.


⸻

▶ How to Run

python main.py sample_images/your_image.png

Real-time Camera Mode

     python camera_capture.py

⸻

 Output Artifacts

After each run, MedTrace generates:

foil_clean.jpg
preprocessed.jpg
ocr_output.jpg
tamper_heatmap.jpg
tamper_output.jpg
cavity_analysis.jpg
ocr_text.txt
verdict.json

These files together form a forensic inspection record.

⸻

 Project Structure

medtrace/
 ├── preprocess.py      # Foil correction
 ├── ocr.py             # OCR + deskew + preprocessing
 ├── tamper.py          # Edge + LBP forensic analysis
 ├── parser.py          # Field extraction
 ├── main.py            # Pipeline runner
 └── sample_images/


⸻

 Forensic JSON Report Example

{
  "drug_name": "PARACETAMOL TABLETS IP",
  "batch_number": "NOT FOUND",
  "expiry_date": "NOT FOUND",
  "tamper_score": 65.09,
  "cavity_deformation_score": 67.66,
  "final_score": 65.86,
  "confidence": "65.86%",
  "evidence": "Surface disturbance and blister cavity deformation detected",
  "verdict": "SUSPICIOUS"
}


⸻

Why This Project Matters

This project simulates techniques used in:
	•	Pharmaceutical packaging inspection
	•	Anti-counterfeit analysis
	•	Surface forensics
	•	Regulatory quality checks

It shows how pure computer vision can extract safety insights from difficult reflective surfaces.

⸻


Limitations & Future Work
	•	Micro-print OCR (batch/expiry) is limited by camera resolution and foil reflectivity
	•	Future improvement: macro-lens capture and super-resolution preprocessing
	•	Possible addition: SSIM comparison against clean foil reference
	•	Potential integration with pharmaceutical packaging inspection workflows



Note: Sample images are used strictly for educational and research demonstration of computer vision techniques. Brand names, if visible, are incidental and not the focus of this project.

⸻