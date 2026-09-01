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

# Wikipedia uses typographic primes: ′ (U+2032) and ″ (U+2033), not ' and "
TIME_PATTERN = re.compile(r"(\d+)\s*h\s*(\d+)\s*[′'`]\s*(?:(\d+)\s*[″\"])?")

def parse_time_hours(value) -> float:
    """
    "94h 33′ 14″" -> 94.5539  (hours as a float)
    Returns NaN for points-based results and missing values.
    """
    text = clean_missing(value)
    if text is np.nan or not isinstance(text, str):
        return np.nan

    match = TIME_PATTERN.search(text)
    if not match:
        return np.nan

    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = int(match.group(3)) if match.group(3) else 0
    return hours + minutes / 60 + seconds / 3600

def parse_points(value) -> float:
    """
    '35' -> 35.0 (early editions were scored on points, not elapsed time)
    Returns NaN when the value is a duration or missing.
    """
    text = clean_missing(value)
    if text is np.nan or not isinstance(text, str):
        return np.nan

    if "h" in text:      # it's a duration, not a point total
        return np.nan
    if re.fullmatch(r"\d+", text.strip()):
        return float(text.strip())
    return np.nan

def parse_rider_name(value) -> dict:
    """
    Extract the rider's name and what the annotation markers mean.

    Wikipedia's legend defines:
      †, #, *, ~ -> the rider also won another classification that year
      [a]-[z]    -> footnote reference
    Rows whose 'name' is actually footnote prose are rejected.
    """
    text = clean_missing(value)
    if text is np.nan or not isinstance(text, str):
        return {"rider_name": np.nan, "multi_classification": False, "no_winner": False}

    multi_classification = any(sym in text for sym in ("#", "†", "*", "~", "&"))

    name = re.sub(r"\[[a-z]\]", "", text)
    name = re.sub(r"[#†*~&]", "", name).strip()
    
    if name.lower().startswith("no winner"):
        return {"rider_name": np.nan, "multi_classification": False, "no_winner": True}

    # Reject footnote prose that isn't a rider name. Real names are short and
    # have no verbs; footnotes are sentences.
    if len(name.split()) > 4 or "not contested" in name.lower():
        return {"rider_name": np.nan, "multi_classification": False, "no_winner": False}

    return {
        "rider_name": name,
        "multi_classification": multi_classification,
        "no_winner": False,
    }

def classify_status(row) -> str:
    """
    Distinguish the three kinds of row:
      'held'     - a normal edition with a winner
      'disputed' - the race happened but the result was annulled (TdF 1999-2005)
      'no_race'  - no edition took place (war years)
    """
    if row.get("no_winner"):
        return "disputed"
    if row.get("rider_name") is np.nan or (isinstance(row.get("rider_name"), float)):
        return "no_race"
    return "held"