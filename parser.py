# parser.py

from rapidfuzz import fuzz
import re

# Expand anytime — system gets smarter automatically
KNOWN_DRUGS = [
    "PARACETAMOL",
    "CAFFEINE",
    "DICLOFENAC",
    "IBUPROFEN",
    "AZITHROMYCIN",
    "AMOXICILLIN",
    "CETIRIZINE",
    "METFORMIN",
]

MONTHS = {
    "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
    "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
    "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"
}


def clean(text):
    return re.sub(r"[^A-Z0-9:/\-. ]", "", text.upper()).strip()


# -------------------- EXPIRY --------------------

def find_expiry(lines):
    for line in lines:
        cl = clean(line)

        # Common pharma formats
        patterns = [
            r"EXP[: ]*\d{2}[/-]\d{2,4}",      # EXP 08/27
            r"EXP[: ]*\d{2}[/-]\d{2}",        # EXP 07-26
            r"\b\d{2}[/-]\d{2,4}\b",         # 08/27
            r"EXP[: ]*[A-Z]{3}[: ]*\d{2,4}", # EXP APR 24
        ]

        for p in patterns:
            m = re.search(p, cl)
            if m:
                val = m.group(0)

                # Convert month word to number
                m2 = re.search(r"([A-Z]{3})[: ]*(\d{2,4})", val)
                if m2:
                    month = MONTHS.get(m2.group(1), "??")
                    year = m2.group(2)
                    return f"{month}/{year}"

                return val.replace("EXP", "").strip()

    return "NOT FOUND"


# -------------------- BATCH --------------------

def find_batch(lines):
    for line in lines:
        cl = clean(line)

        patterns = [
            r"B\.?NO[: ]*[A-Z0-9]+",     # B.NO MH0437
            r"BATCH[: ]*[A-Z0-9]+",     # BATCH 45821X
            r"BN[: ]*[A-Z0-9]+",        # BN 22K91
            r"LOT[: ]*[A-Z0-9]+",       # LOT 4582A
            r"\b[A-Z]{1,3}\d{3,6}[A-Z]?\b"  # MH0437, 22K91
        ]

        for p in patterns:
            m = re.search(p, cl)
            if m:
                val = m.group(0)

                # Clean prefix if present
                val = re.sub(r"(B\.?NO|BATCH|BN|LOT)[: ]*", "", val)
                return val.strip()

    return "NOT FOUND"


# -------------------- DRUG NAME (SMART) --------------------

def fuzzy_match_drug(lines):
    best_match = ("UNKNOWN", 0)

    for line in lines:
        cl = clean(line)

        for drug in KNOWN_DRUGS:
            score = fuzz.partial_ratio(cl, drug)

            if score > best_match[1]:
                best_match = (drug, score)

    if best_match[1] > 70:
        return best_match[0]

    return "UNKNOWN"


def heuristic_drug_line(lines):
    for line in lines:
        cl = clean(line)

        if (
            10 < len(cl) < 60 and
            any(w in cl for w in ["TABLET", "TABLETS", "CAPSULE", "IP"])
        ):
            return cl

    return None


# -------------------- MAIN PARSER --------------------

def parse_fields(ocr_texts):
    # 1) Try fuzzy match first (robust to OCR errors)
    drug_name = fuzzy_match_drug(ocr_texts)

    # 2) If fuzzy fails, fallback to heuristic
    if drug_name == "UNKNOWN":
        h = heuristic_drug_line(ocr_texts)
        drug_name = h if h else "UNKNOWN"

    return {
        "drug_name": drug_name,
        "batch_number": find_batch(ocr_texts),
        "expiry_date": find_expiry(ocr_texts),
    }