# Findings — Grand Tours Analysis

Standalone summary. Full working in [`notebooks/04_analysis.ipynb`](../notebooks/04_analysis.ipynb).

**Scope**: 333 race-editions — Tour de France (1903–2026), Giro d'Italia (1909–2026),
Vuelta a España (1935–2025) — with biographical data for 156 of 161 winners.

---

## Headline

**The three Grand Tours have converged on every measurable dimension, but they did not get
there together.** Distance, speed and national openness all narrowed across the century, yet
year-on-year the races show no co-movement at all. The convergence is independent drift toward
a shared constraint, not coordination.

---

## Convergence

| Dimension | Early | Now |
| --- | --- | --- |
| Distance | 2,000+ km apart (1920s) | within ~200 km |
| Speed | 4+ km/h apart (1930s–50s) | within ~2 km/h since 1980 |
| National concentration | Giro 1.000, Tour 0.34 | all 0.2–0.4 by the 1980s |

**But not together.** Raw distances correlate at r = 0.565 (Giro–Tour) — a shared time trend.
After differencing, year-on-year changes correlate at |r| < 0.2 for every pair. The Vuelta
correlates with neither race even in raw form (0.046, 0.056); it fell through the 1950s and
rose again in the 1970s–80s while the Tour was still shrinking.

## National dominance

Italy 84 wins, France 51, Spain 48, Belgium 33.

**The home-race effect is overwhelming**: Italy takes 81% of its wins at the Giro, France 71%
at the Tour, Spain 67% at the Vuelta. Belgium, with no home Grand Tour, spreads its 33 wins
evenly (18/7/8) — suggesting the effect comes from riders targeting their national race, not
from terrain.

**The Giro was closed for forty years.** Its concentration index sits at exactly 1.000 from the
1910s to the 1940s — every winner Italian, without exception. No other race approaches this.

**Current divergence.** In the 2010s the Giro and Vuelta reached their most open ever (0.22,
0.20) while the Tour tightened (0.40 → 0.59 in the 2020s), concentrated on Pogačar and
Vingegaard. The most prestigious race is now the least nationally diverse.

## Riders

**Most wins**: Merckx 11, Hinault 10, Anquetil 8, Contador and Froome 7 each.

**Eight riders have won all three Grand Tours**, in two clusters separated by 28 years:
Anquetil (1963), Gimondi (1968), Merckx (1973), Hinault (1980) — then nothing until Contador
(2008), Nibali (2014), Froome (2018), Vingegaard (2026). The gap coincides with cycling's era
of extreme specialisation.

**Cross-era comparison is not possible.** The eight most successful riders sort almost perfectly
by era when ranked on speed (Binda 27.1 km/h → Pogačar 42.1). Plotted against all editions, every
one sits at the top of their own era and none is a dramatic outlier. The differences are
equipment and road surfaces, not physiology.

## Age

Mean 27.9, median 27.7, sd 3.3. Half of all victories come from riders aged 25.6–30.2.

**Winners are getting older — by 1.95 years across the whole history.** Permutation test
(5,000 shuffles): p = 0.0008. Only 4 shuffles produced a slope this steep.

**The effect is real and small.** r² = 0.038 — the year explains under 4% of the variation in
winning age. Both facts belong in the reporting.

**Extremes**: Chris Horner won the 2013 Vuelta at 41.9, over five years older than any other
winner. Henri Cornet (19.97, 1904) and Fausto Coppi (20.71, 1940) are the only winners under 21.

---

## Methodological notes

- **Differencing separates shared trends from real relationships.** Two series that both decline
  over a century correlate whether or not they are related. Correlating changes rather than
  levels is what turned an apparent Giro–Tour relationship (0.565) into its true value (0.160).
- **Significance is not size.** p = 0.0008 with r² = 0.038.
- **Validation against known facts catches silent errors.** Checking "eight riders won all three"
  against our result of six exposed two scraping bugs: a fifth marker symbol, and reassigned
  titles encoded as strikethrough HTML rather than notation. The dataset had looked entirely
  reasonable while missing two riders' Vuelta wins.
- **Status is not binary.** Four categories (`held`/`disputed`/`no_race`/`team_only`) let each
  question filter correctly. A single validity flag would have either dropped seven Tours that
  genuinely happened or counted seven winners who do not exist.

## Limitations

- Winner-level data only — no field data, so rider dominance cannot be separated from weak years.
- 96.9% Wikidata match rate; age analysis covers 288 of 294 held editions.
- Nationality is licence nationality, which conflicts with Wikidata citizenship for historical
  states and dual nationals.
- Doping is unmodelled; results reflect current official standings.
- No stage-level data. Climbing metres and mountain-stage counts would sharpen the speed analysis
  considerably and are the obvious next step.
