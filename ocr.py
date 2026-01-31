# ocr.py

import easyocr
import cv2
import numpy as np

# Load OCR model once
reader = easyocr.Reader(['en'])


def deskew(image):
    """
    Automatically rotates the image to correct tilt.
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


def run_ocr(image):
    """
    Runs OCR on an already preprocessed image.
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

    cv2.imwrite("ocr_output.jpg", image)

    return extracted_texts