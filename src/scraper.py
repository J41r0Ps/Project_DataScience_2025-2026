import re
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GrandToursAnalysis/1.0 (educational data science project)"}

RACE_URLS = {
    "tdf": "https://en.wikipedia.org/wiki/List_of_Tour_de_France_general_classification_winners",
    "giro": "https://en.wikipedia.org/wiki/List_of_Giro_d%27Italia_general_classification_winners",
    "vuelta": "https://en.wikipedia.org/wiki/List_of_Vuelta_a_Espa%C3%B1a_general_classification_winners",
}

# Maps many possible header spellings onto one canonical field name.
COLUMN_ALIASES = {
    "year": "year",
    "country": "country",
    "cyclist": "cyclist",
    "sponsor/team": "team",
    "distance": "distance",
    "time/points": "time_points",
    "time": "time_points",
    "margin": "margin",
    "stage wins": "stage_wins",
}


def get_soup(url: str, delay: float = 1.0) -> BeautifulSoup:
    """Fetch a page and return parsed soup. Delay keeps us polite to Wikipedia."""
    time.sleep(delay)
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.content, "lxml")


def normalise_header(text: str) -> str:
    """
    'Sponsor / team' -> 'sponsor/team'
    'Time/Points'    -> 'time/points'
    Collapses whitespace around slashes so the three races' spellings unify.
    """
    text = text.strip().lower()
    text = re.sub(r"\s*/\s*", "/", text)   # normalise spacing around slashes
    text = re.sub(r"\s+", " ", text)        # collapse remaining whitespace
    return text

def get_column_map(table) -> dict[int, str]:
    """
    Read the table's header row and return {column_index: canonical_field_name}.
    Unknown headers are skipped, so extra columns never break parsing.
    """
    header_row = table.find("tr")
    header_cells = header_row.find_all(["th", "td"])

    column_map = {}
    for i, cell in enumerate(header_cells):
        key = normalise_header(cell.get_text())
        if key in COLUMN_ALIASES:
            column_map[i] = COLUMN_ALIASES[key]
    return column_map


def parse_winners_table(table, race: str) -> list[dict]:
    """
    Parse the main 'winners by year' table into a list of raw dicts.
    Values are kept as raw text — cleaning happens in 02_cleaning.
    """
    column_map = get_column_map(table)
    rows = table.find_all("tr")[1:]  # skip header row

    records = []
    for row in rows:
        # Data rows mix <th> (cyclist name) and <td> (everything else),
        # so we collect both in document order to keep indices aligned.
        cells = row.find_all(["th", "td"])
        if not cells:
            continue

        record = {"race": race}
        for i, cell in enumerate(cells):
            field = column_map.get(i)
            if not field:
                continue

            # A struck-through name means the title was stripped and reassigned.
            # Record that fact, then remove the struck text so only the
            # current title-holder's name survives.
            struck = cell.find_all(["s", "del", "strike"])
            if struck and field == "cyclist":
                record["title_reassigned"] = True
                for tag in struck:
                    tag.decompose()

            record[field] = cell.get_text(strip=True)

        record.setdefault("title_reassigned", False)

        # a valid row must at least have a year
        if record.get("year"):
            records.append(record)

    return records

def scrape_race(race: str, delay: float = 1.0) -> list[dict]:
    """Scrape one race's winners table."""
    if race not in RACE_URLS:
        raise ValueError(f"Unknown race {race!r}. Options: {list(RACE_URLS)}")

    soup = get_soup(RACE_URLS[race], delay=delay)
    tables = soup.find_all("table", class_="wikitable")
    records = parse_winners_table(tables[1], race)
    print(f"{race}: {len(records)} rows")
    return records


def scrape_all_races(delay: float = 1.0) -> list[dict]:
    """Scrape all three Grand Tours."""
    all_records = []
    for race in RACE_URLS:
        all_records.extend(scrape_race(race, delay=delay))
    return all_records