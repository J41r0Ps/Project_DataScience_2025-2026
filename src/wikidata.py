import time
import numpy as np
import requests

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": "GrandToursAnalysis/1.0 (educational data science project)",
    "Accept": "application/sparql-results+json",
}

QUERY_TEMPLATE = """
SELECT ?name ?riderLabel ?birthDate ?countryLabel ?height ?weight WHERE {{
  VALUES ?name {{ {names} }}
  {{ ?rider rdfs:label ?name . }}
  UNION
  {{ ?rider skos:altLabel ?name . }}
  ?rider wdt:P106 wd:Q2309784 .
  ?rider wdt:P569 ?birthDate .
  OPTIONAL {{ ?rider wdt:P27 ?country . }}
  OPTIONAL {{ ?rider wdt:P2048 ?height . }}
  OPTIONAL {{ ?rider wdt:P2067 ?weight . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
"""

NAME_ALIASES = {
    "Miguel Indurain": "Miguel Induráin",
}


def build_query(names: list[str]) -> str:
    """Build a SPARQL query for a batch of rider names."""
    escaped = " ".join(f'"{n.replace(chr(34), "")}"@en' for n in names)
    return QUERY_TEMPLATE.format(names=escaped)


def run_query(query: str, delay: float = 1.0) -> list[dict]:
    """Send a SPARQL query and return the raw result bindings."""
    time.sleep(delay)
    response = requests.get(
        SPARQL_ENDPOINT, params={"query": query, "format": "json"},
        headers=HEADERS, timeout=60,
    )
    response.raise_for_status()
    return response.json()["results"]["bindings"]


def normalise_height(value) -> float:
    """
    Wikidata mixes units: some riders' heights are stored in metres (1.82),
    others in centimetres (186). Values below 3 are assumed to be metres.
    """
    if value is None:
        return np.nan
    value = float(value)
    return value * 100 if value < 3 else value


def parse_binding(binding: dict) -> dict:
    """Flatten one SPARQL result row into a plain dict."""
    def get(key):
        return binding[key]["value"] if key in binding else None

    return {
        "query_name": get("name"),
        "wikidata_label": get("riderLabel"),
        "birth_date": get("birthDate"),
        "country_wikidata": get("countryLabel"),
        "height_cm": normalise_height(get("height")),
        "weight_kg": float(get("weight")) if get("weight") else np.nan,
    }


def fetch_riders(names: list[str], batch_size: int = 50, delay: float = 1.0) -> list[dict]:
    """
    Fetch Wikidata facts for a list of rider names, in batches.
    Batching keeps each query under the endpoint's complexity limits.
    """
    results = []
    for start in range(0, len(names), batch_size):
        batch = names[start:start + batch_size]
        bindings = run_query(build_query(batch), delay=delay)
        results.extend(parse_binding(b) for b in bindings)
        print(f"batch {start // batch_size + 1}: {len(batch)} names -> {len(bindings)} rows")
    return results

def resolve_name(name: str) -> str:
    """Map known Wikipedia spelling variants onto their Wikidata label."""
    return NAME_ALIASES.get(name, name)

def resolve_duplicates(rows: list[dict], ambiguous_names: set[str]) -> list[dict]:
    """
    Drop rows for names that matched multiple distinct people.
    Ambiguity is reported rather than resolved by guessing.
    """
    return [r for r in rows if r["query_name"] not in ambiguous_names]