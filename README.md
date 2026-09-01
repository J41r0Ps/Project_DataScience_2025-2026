# 🚴 Grand Tours Analysis

> A complete data pipeline over 120 years of professional cycling — scraping, cleaning, API
> enrichment and statistical analysis of the Tour de France, Giro d'Italia and Vuelta a España.

**333 race-editions · 161 riders · 1903–2026 · 10 research questions**

---

## 📊 Headline finding

**The three Grand Tours have converged on every measurable dimension — but they did not get
there together.**

| Dimension | Early | Now |
| --- | --- | --- |
| Distance | 2,000+ km apart (1920s) | within ~200 km |
| Winning speed | 4+ km/h apart (1930s–50s) | within ~2 km/h since 1980 |
| National concentration | Giro 1.000 (every winner Italian for 40 years) | all 0.2–0.4 by the 1980s |

Yet after removing the shared century-long trend, year-on-year changes in distance correlate at
|r| < 0.2 across every pair of races. The convergence is independent drift toward a common
constraint — most plausibly UCI regulation — not coordination between organisers.

Full write-up: **[`docs/FINDINGS.md`](docs/FINDINGS.md)**

---

## 🎯 About this project

This is a **rebuild and expansion** of a course project for the Data Science course at
Thomas More (2APPAI). The original brief prohibited Pandas and covered only the Tour de France,
so the first version used raw Python lists, NumPy and Matplotlib, producing four disconnected
data files — one shaped around each research question.

| Original | This version |
| --- | --- |
| Tour de France only | All three Grand Tours, with cross-race comparison |
| No Pandas (brief prohibited it) | Full Pandas pipeline with a tidy relational data model |
| 4 disconnected files, no shared keys | Two joined tables: `editions` + `riders` |
| All logic inline in notebooks | Reusable `src/` package with 28 unit tests |
| Birth dates scraped from ~100 rider pages | Wikidata SPARQL — structured, batched, 3 requests |
| Age = winning year − birth year | Exact age from race end dates |
| Winning times compared across eras | Average speed, with the era confound made explicit |
| Descriptive observations | Permutation tests, differencing, concentration indices |

The original notebooks are preserved in [`legacy/`](legacy/) as a deliberate before/after.

---

## 🚀 Quick start

**Want to run the analysis without scraping anything?** The processed datasets are published in
this repo. Clone it and open `notebooks/04_analysis.ipynb` — it reads directly from
`data/processed/` and runs in seconds.

```bash
git clone https://github.com/J41r0Ps/grand-tours-analysis.git
cd grand-tours-analysis
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
jupyter notebook
```

**Want to rebuild the data from source?** Run notebooks `01` → `03` first. The full pipeline
takes a few minutes: `01` scrapes three Wikipedia pages, `03` makes four batched SPARQL queries.

Run the tests with `pytest`.

---

## 📦 Published datasets

Both files are in `data/processed/` and licensed **CC BY-SA 4.0**. Schema and known issues:
[`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md).

**`editions_enriched.csv`** — 333 rows × 18 columns, one per race-edition
`race · year · rider_name · country · team · distance_km · winning_time_hours · winning_points ·
avg_speed_kmh · age_at_win · status · multi_classification · title_reassigned · height_cm · weight_kg …`

**`riders_enriched.csv`** — 161 rows × 11 columns, one per rider
`rider_name · country · wins_tdf · wins_giro · wins_vuelta · wins_total · races_won ·
birth_date · citizenships · height_cm · weight_kg`

### The `status` column is the important one

| Value | Rows | Meaning |
| --- | --- | --- |
| `held` | 294 | Normal edition with a winner |
| `no_race` | 23 | No edition took place (world wars) |
| `disputed` | 7 | TdF 1999–2005 — raced, result annulled |
| `team_only` | 1 | 1912 Giro — team classification only |

Disputed editions have routes and distances, so they belong in route-level analysis but not in
win counts. A single valid/invalid flag would force a wrong answer to one of those questions.

---

## 🗂️ Data sources

| Source | Type | Provides | Licence |
| --- | --- | --- | --- |
| Wikipedia GC winners tables (×3) | Scraping (BeautifulSoup) | year, winner, country, team, distance, time/points | CC BY-SA 4.0 |
| [Wikidata](https://query.wikidata.org/) | SPARQL API | birth dates, citizenship, height, weight | CC0 |

**The scraper maps columns by header name, not position.** The three pages spell the same
columns differently (`Sponsor/Team`, `Sponsor / team`, `Sponsor/team`; `Time/Points`,
`Time / points`, `Time`), so one normalised lookup handles all three races and tolerates
Wikipedia adding or reordering columns.

---

## 🧬 Pipeline

| Stage | Notebook | Output |
| --- | --- | --- |
| **Obtain** | `01_scraping.ipynb` | `data/raw/grand_tours_raw.csv` |
| **Scrub** | `02_cleaning.ipynb` | `editions.csv`, `riders.csv` |
| **Enrich** | `03_enrichment.ipynb` | `editions_enriched.csv`, `riders_enriched.csv` |
| **Explore** | `04_analysis.ipynb` | 10 questions, charts, findings |

```
grand-tours-analysis/
├── data/processed/ # published datasets (CC BY-SA 4.0)
├── notebooks/ # 01 scraping → 04 analysis
├── src/
│ ├── scraper.py # generalised Wikipedia table scraper
│ ├── cleaning.py # regex parsers, status classification
│ └── wikidata.py # SPARQL client
├── tests/ # 28 pytest unit tests
├── legacy/ # original course submission
├── docs/ # data dictionary, findings
├── LICENSE # MIT (code)
└── DATA_LICENSE.md # CC BY-SA 4.0 (data)
```

---

## ❓ Research questions

**Rebuilt from the original:** nationality counts · most successful riders · distance evolution ·
rider comparison · winning age

**New, enabled by the expanded scope:** cross-race distance correlation · speed convergence ·
riders who won all three · whether the age trend is statistically meaningful · eras of national
dominance

---

## 🛠️ Techniques

| Area | Techniques |
| --- | --- |
| Scraping | requests + BeautifulSoup, header-name column mapping, strikethrough extraction via `decompose()`, multi-source generalisation |
| API | Wikidata SPARQL, batched `VALUES` queries, `UNION` over `rdfs:label` and `skos:altLabel`, occupation filtering for disambiguation |
| Cleaning | Regex parsing (typographic primes, thousands separators), em-dash placeholder handling, four-way status classification, unit normalisation |
| Analysis | Pandas groupby/merge/pivot, NumPy aggregations, correlation with differencing, permutation testing, `polyfit` trend fitting, Herfindahl concentration index |
| Visualisation | Matplotlib + Seaborn, jersey-coloured race palette, rolling medians, career timelines, small multiples |
| Engineering | Modular `src/` package, 28 pytest tests, checkpointed pipeline, output validation cells |

---

## 🐛 Two bugs worth reading about

**Validation against a known fact caught a silent error.** Wikipedia states eight riders have won
all three Grand Tours. The pipeline returned six. Chasing that gap exposed a fifth marker symbol
(`&`, used only on the Vuelta page) and — more interestingly — that reassigned titles are encoded
as **strikethrough HTML**, not notation:

```html
<th><s>Juan José Cobo</s> Chris Froome</th>
```

`get_text()` flattens that into `"Juan José CoboChris Froome"`. The fix removes struck elements
with `decompose()` before extracting text, and records their presence as `title_reassigned`.

Without the external check, the dataset would have looked entirely reasonable while missing
Merckx's and Froome's Vuelta wins. Details in `notebooks/02_cleaning.ipynb`.

---

## 📄 Licence

Code: **MIT** ([`LICENSE`](LICENSE)) · Data: **CC BY-SA 4.0** ([`DATA_LICENSE.md`](DATA_LICENSE.md))

Data derives from Wikipedia (CC BY-SA 4.0) and Wikidata (CC0). Share-alike propagates: please
attribute both Wikipedia and this repository, and release modifications under the same terms.

---

## 👤 Author

Data Science portfolio ***Jairo Nacurena Tuy*** — Applied Computer Science, Thomas More Geel.
