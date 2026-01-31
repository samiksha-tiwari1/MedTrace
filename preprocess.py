# preprocess.py

import cv2
import numpy as np


def clean_foil(image_path):
    """
    Cleans reflective foil surface for better OCR and texture analysis.

    Steps:
    - Grayscale conversion
    - Contrast normalization (CLAHE)
    - Bilateral filtering (reduce glare noise, keep edges)
    - Morphological opening (remove foil speckles)
    """

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Contrast normalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    norm = clahe.apply(gray)

    # Reduce glare noise but preserve text edges
    smooth = cv2.bilateralFilter(norm, 9, 75, 75)

    # Remove tiny foil specks
    kernel = np.ones((3, 3), np.uint8)
    clean = cv2.morphologyEx(smooth, cv2.MORPH_OPEN, kernel)

    cv2.imwrite("foil_clean.jpg", clean)

    return clean