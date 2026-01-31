# tamper.py

import cv2
import numpy as np
from skimage.feature import local_binary_pattern


def detect_tamper(image):
    """
    Forensic tamper detection on medicine foil using:

    1) Edge density  -> scratches / overprints
    2) LBP variance  -> micro texture disturbance

    Outputs:
        tamper_heatmap.jpg
        tamper_output.jpg
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ---------------- Edge Detection ----------------
    edges = cv2.Canny(gray, 100, 200)
    edge_score = np.sum(edges) / edges.size

    # Heatmap for visualization
    heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
    cv2.imwrite("tamper_heatmap.jpg", heatmap)

    # ---------------- LBP Texture Analysis ----------------
    lbp = local_binary_pattern(gray, P=8, R=1, method="uniform")
    lbp_score = np.var(lbp)

    # ---------------- Proper Normalization (0–1 range) ----------------
    edge_norm = min(1.0, edge_score * 5)
    lbp_norm = min(1.0, np.log(1 + lbp_score) / 10)

    # Combine into 0–100 forensic score
    final_score = (0.6 * edge_norm + 0.4 * lbp_norm) * 100

    # ---------------- Locate Suspicious Region ----------------
    h, w = edges.shape
    block_size = 60
    max_block_score = 0
    suspicious_block = None

    for y in range(0, h - block_size, block_size):
        for x in range(0, w - block_size, block_size):
            block = edges[y:y + block_size, x:x + block_size]
            score = np.sum(block)

            if score > max_block_score:
                max_block_score = score
                suspicious_block = (x, y)

    # Mark suspicious region
    if suspicious_block:
        x, y = suspicious_block
        cv2.rectangle(
            image,
            (x, y),
            (x + block_size, y + block_size),
            (0, 0, 255),
            3
        )

    cv2.imwrite("tamper_output.jpg", image)

    return float(final_score)