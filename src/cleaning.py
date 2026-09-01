import re
import numpy as np

# Wikipedia uses an em-dash for "no data", not an empty cell
MISSING_MARKERS = {"—", "–", "-", ""}


def clean_missing(value):
    """Convert Wikipedia's em-dash placeholders into real NaN."""
    if value is None:
        return np.nan
    text = str(value).strip()
    return np.nan if text in MISSING_MARKERS else text

def parse_distance(value) -> float:
    """
    '2,428km (1,509mi)' -> 2428.0
    Takes the kilometre figure, drops the thousands separator and the miles conversion.
    """
    text = clean_missing(value)
    if text is np.nan or not isinstance(text, str):
        return np.nan

    match = re.search(r"([\d,]+(?:\.\d+)?)\s*km", text)
    if not match:
        return np.nan
    return float(match.group(1).replace(",", ""))