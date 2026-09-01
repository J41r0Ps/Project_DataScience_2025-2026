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

