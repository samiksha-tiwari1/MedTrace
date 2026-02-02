"""
camera_capture.py

MedTrace — Real-time Forensic Inspection via Camera

Features:
✔ HD camera capture
✔ Autofocus delay before capture
✔ Runs MedTrace pipeline automatically
✔ Overlays forensic verdict on captured image
✔ Intelligent advisory when micro-print OCR is unreliable
"""

import cv2
import json
import subprocess
import time


def show_result_on_frame(image_path):
    """
    Reads verdict.json and overlays the forensic
    inspection results directly onto the image.
    """

    # Load result
    with open("verdict.json", "r") as f:
        result = json.load(f)

    image = cv2.imread(image_path)

    # Main inspection lines
    lines = [
        f"Drug: {result['drug_name']}",
        f"Batch: {result['batch_number']}",
        f"Expiry: {result['expiry_date']}",
        f"Verdict: {result['verdict']}",
        f"Score: {result['confidence']}",
    ]

    # Add intelligent forensic advisory
    if result["batch_number"] == "NOT FOUND" or result["expiry_date"] == "NOT FOUND":
        lines.append("⚠ Micro-print region detected.")
        lines.append("Resolution insufficient for reliable OCR.")
        lines.append("Try high-resolution still image upload.")

    # Draw text on image
    y = 40
    for line in lines:

        # Red for main info, orange for advisory
        color = (0, 0, 255)
        if (
            "Micro-print" in line
            or "Resolution" in line
            or "high-resolution" in line
        ):
            color = (0, 165, 255)

        cv2.putText(
            image,
            line,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            color,
            2,
        )
        y += 35

    cv2.imshow("MedTrace Inspection Result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def capture_and_run():
    """
    Opens camera, captures image on SPACE,
    runs MedTrace, and displays result.
    """

    cap = cv2.VideoCapture(0)

    # Force HD resolution for better OCR
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    print("📷 MedTrace Camera Active")
    print("➡️  Press SPACE to capture")
    print("❌ Press ESC to exit")

    while True:
        ret, frame = cap.read()
        cv2.imshow("MedTrace Live Camera", frame)

        key = cv2.waitKey(1)

        # SPACE → capture
        if key % 256 == 32:
            print("Hold still... capturing in 2 seconds for autofocus")
            time.sleep(2)

            ret, frame = cap.read()

            image_path = "captured.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Saved as {image_path}")
            break

        # ESC → exit
        elif key % 256 == 27:
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()

    print("🔍 Running MedTrace forensic inspection...")
    subprocess.run(["python", "main.py", image_path])

    # Wait to ensure verdict.json is written
    time.sleep(1)

    show_result_on_frame(image_path)


if __name__ == "__main__":
    capture_and_run()