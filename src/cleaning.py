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
    Extract the rider's name plus what the annotation markers tell us.

    'Henri Cornet[b]'      -> name='Henri Cornet',      reassigned=False, no_winner=False
    'Andy Schleck#[e]'     -> name='Andy Schleck',      reassigned=True,  no_winner=False
    'Michele Scarponi†[a]' -> name='Michele Scarponi',  reassigned=True,  no_winner=False
    'No winner[a]'         -> name=NaN,                 reassigned=False, no_winner=True
    '—'                    -> name=NaN,                 reassigned=False, no_winner=False
    """
    text = clean_missing(value)
    if text is np.nan or not isinstance(text, str):
        return {"rider_name": np.nan, "is_reassigned": False, "no_winner": False}

    # '#' and '†' both mark a title awarded after the original winner was stripped
    reassigned = "#" in text or "†" in text

    # strip footnote refs [a]-[z] and the status symbols
    name = re.sub(r"\[[a-z]\]", "", text)
    name = name.replace("#", "").replace("†", "").strip()

    if name.lower().startswith("no winner"):
        return {"rider_name": np.nan, "is_reassigned": False, "no_winner": True}

    return {"rider_name": name, "is_reassigned": reassigned, "no_winner": False}

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