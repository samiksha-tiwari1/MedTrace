# parser.py

import re


def parse_fields(ocr_texts):
    """
    Extract likely drug name, batch number, and expiry date
    from noisy OCR output.
    """

    full_text = " ".join(ocr_texts).upper()

    # Date patterns like 07/25, 08-2026
    date_pattern = r'\b\d{2}[\/\-]\d{2,4}\b'
    dates_found = re.findall(date_pattern, full_text)
    expiry_date = dates_found[-1] if dates_found else "NOT FOUND"

    # Batch-like alphanumeric pattern
    batch_pattern = r'\b[A-Z]{1,3}\d{3,6}\b'
    batch_match = re.search(batch_pattern, full_text)
    batch_number = batch_match.group(0) if batch_match else "NOT FOUND"

    # Longest line heuristic for drug name
    drug_name = max(ocr_texts, key=len) if ocr_texts else "UNKNOWN"

    return {
        "drug_name": drug_name,
        "batch_number": batch_number,
        "expiry_date": expiry_date
    }