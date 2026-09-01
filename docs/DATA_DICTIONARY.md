# Data Dictionary — Grand Tours Analysis

Two published datasets, both derived from Wikipedia and Wikidata. Licence: CC BY-SA 4.0
(see [`DATA_LICENSE.md`](../DATA_LICENSE.md)).

---

## `data/processed/editions_enriched.csv` — 333 rows × 18 columns

One row per race-edition, including years when no race was held.

| Column | Type | Description |
| --- | --- | --- |
| `race` | str | `tdf`, `giro` or `vuelta` |
| `year` | int | Year the edition was held |
| `rider_name` | str | Winner, markers stripped. `NaN` where there is no winner |
| `country` | str | Nationality as shown in the results table (licence nationality) |
| `team` | str | Sponsor / trade team |
| `distance_km` | float | Race distance in km |
| `winning_time_hours` | float | Winner's total time in hours. `NaN` for points-scored editions |
| `winning_points` | float | Winner's point total. `NaN` for time-scored editions |
| `avg_speed_kmh` | float | `distance_km / winning_time_hours` |
| `multi_classification` | bool | Winner also took another classification (points/mountains/young rider) |
| `title_reassigned` | bool | Title awarded after the original winner was stripped |
| `no_winner` | bool | Race held, result annulled |
| `status` | str | `held` / `disputed` / `no_race` / `team_only` — see below |
| `birth_date` | datetime | Winner's date of birth (Wikidata) |
| `age_at_win` | float | Age in years at the race end date |
| `height_cm` | float | Winner's height (Wikidata) |
| `weight_kg` | float | Winner's mass (Wikidata) |
| `citizenships` | str | Comma-separated citizenships (Wikidata) |

### The `status` column

| Value | Rows | Meaning |
| --- | --- | --- |
| `held` | 294 | Normal edition with a winner |
| `no_race` | 23 | No edition took place (world wars) |
| `disputed` | 7 | TdF 1999–2005: raced, result annulled |
| `team_only` | 1 | 1912 Giro: team classification only, no individual winner |

**This distinction is the point.** `disputed` editions have routes and distances and belong in
any route-level analysis; they have no winner and must be excluded from win counts. `no_race`
belongs in neither. A single valid/invalid flag would force a wrong choice on one of these.

---

## `data/processed/riders_enriched.csv` — 161 rows × 11 columns

One row per rider who has won at least one Grand Tour.

| Column | Type | Description |
| --- | --- | --- |
| `rider_name` | str | Canonical name (join key to `editions_enriched`) |
| `country` | str | Nationality from their first recorded win |
| `wins_tdf` / `wins_giro` / `wins_vuelta` | int | Wins per race |
| `wins_total` | int | Total Grand Tour wins |
| `races_won` | int | How many *different* Grand Tours (1–3) |
| `birth_date` | datetime | Wikidata |
| `citizenships` | str | Comma-separated; may include historical states |
| `height_cm` | float | Normalised to cm |
| `weight_kg` | float | Wikidata |

---

## Known data issues

| Issue | Detail |
| --- | --- |
| **Wikidata coverage** | 156/161 riders matched (96.9%). Five unmatched (accent and transliteration variants); two excluded as ambiguous (*Aitor González*, *Alexander Vinokourov* each match two cyclists). Age analysis covers 288/294 held editions. |
| **Nationality vs citizenship** | `country` is licence nationality from the results table. `citizenships` is Wikidata and often conflicts: pre-1946 Italians hold *Italy* and *Kingdom of Italy*; Soviet-era riders *Russia* and *Soviet Union*; Chris Froome *Kenya* and *United Kingdom*. Use `country` for counting wins. |
| **Height units** | Wikidata stores some heights in metres and others in centimetres. Values below 3 are treated as metres and converted. |
| **Points vs time** | Early editions (TdF 1905–1912, Giro pre-1914) were scored on points. `winning_time_hours` and `avg_speed_kmh` are `NaN` for those years. |
| **Marker symbols** | Wikipedia's tables use at least seven annotation symbols (`†`, `#`, `*`, `~`, `&`, `‡`, `§`) plus `[a]`–`[z]` footnotes. All are stripped; the classification symbols are captured in `multi_classification`. |
| **Doping** | Results are recorded as they now officially stand, which is not what happened on the road. |
