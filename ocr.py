# ocr.py

import easyocr
import cv2
import numpy as np

# Load OCR model once
reader = easyocr.Reader(['en'])


def deskew(image):
    """
    Automatically rotates the image to correct tilt.
    Improves OCR accuracy significantly.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(
        image,
        M,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def run_roi_ocr(image):
    """
    Second OCR pass for tiny batch/expiry text.
    Crops bottom-right region, zooms, and enhances it.
    """

    h, w, _ = image.shape

    # Crop region where batch/expiry usually printed
    roi = image[int(h * 0.6):h, int(w * 0.5):w]

    # Enlarge ROI to help OCR read tiny text
    roi = cv2.resize(roi, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Strong threshold for dot-matrix print
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Save for debugging / README evidence
    cv2.imwrite("roi_zoom.jpg", thresh)

    results = reader.readtext(thresh)

    roi_texts = [text for (_, text, _) in results]

    return roi_texts


def run_ocr(image):
    """
    Full OCR pipeline:
    1) Deskew
    2) Preprocess
    3) Full-strip OCR
    4) ROI OCR for batch/expiry
    """

    # 🔄 Auto straighten
    image = deskew(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    processed = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        5
    )

    cv2.imwrite("preprocessed.jpg", processed)

    # -------- First Pass OCR (whole strip) --------
    results = reader.readtext(processed)

    extracted_texts = []

    for (bbox, text, prob) in results:
        extracted_texts.append(text)

        pts = [tuple(map(int, point)) for point in bbox]
        cv2.polylines(image, [np.array(pts)], True, (0, 255, 0), 2)
        cv2.putText(
            image,
            text,
            pts[0],
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # -------- Second Pass OCR (tiny text) --------
    roi_texts = run_roi_ocr(image)
    extracted_texts.extend(roi_texts)

    # Save OCR visual
    cv2.imwrite("ocr_output.jpg", image)

    return extracted_texts