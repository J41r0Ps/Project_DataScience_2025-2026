# 🚴 Tour de France Data Science Project

## Introduction

This project demonstrates a complete data science workflow centered around the multi-stage cycling race Tour de France. The goal is to gain hands-on experience with scraping, cleaning, Pythonic data analysis, and clear communication—skills essential for roles like data engineer, data scientist, or AI consultant.

All data was collected via web scraping (BeautifulSoup) from publicly available datasets in the [LeTourDataSet GitHub project](https://github.com/EloiNavet/LeTourDataSet/tree/master/data). Data manipulation is done **without pandas** (pure Python using list comprehensions, map, filter, Counter, etc.), making the code more universal and educational.

## Objectives

- Showcase end-to-end data science skills: from data scraping to processed insights
- Deep exploration of statistics from historical Tour de France data
- Emphasis on “Pythonic” programming techniques, clear explanations (markdown/comments), and real-world data quality control (data cleaning)
- Transparent documentation: every step, method, and decision is clearly communicated

## Data

**Source:** [LeTourDataSet/data](https://github.com/EloiNavet/LeTourDataSet/tree/master/data)  
**Files used:**

- `TDF_Riders_History.csv`: Info about winners, teams, years, nationalities
- `TDF_Stages_History.csv`: Stage data (distance, date, year)
- Other files may be used as supplements

**Collection method:**  
Tables were scraped directly from HTML pages using BeautifulSoup. Cleaning and type conversion were applied to produce a reliable model sample. Clean data is exported as CSV.

## Project Structure

```
├── README.md
├── 01_scraping_cleaning.ipynb # Scraping en data cleaning workflow
├── 02_analysis.ipynb # Analyse per onderzoeksvraag
├── data/
│ ├── cleaned_riders.csv
│ ├── cleaned_stages.csv
│ └── ... (ruwe/extra data)
├── .gitignore
```

## Research Questions & Methods

This project answers the following five relevant questions based on the data, in a fully reproducible way:

1. **Who was the most frequent winner?**  
   Scraping + cleaning of `TDF_Riders_History.csv`, using Python’s Counter for frequency counting.

2. **How many stages were raced per year?**  
   Analysis of `TDF_Stages_History.csv`, grouped and counted by year.

3. **What is the average stage length per decade?**  
   Distance cleaning, grouping by decade, calculating averages.

4. **Which nationalities appeared most often on the podium?**  
   Filtering top-3 positions and grouping by nationality.

5. **Which teams had the most victories since 2000?**  
   Filtering by team/year and sorting winners per team post-2000.

Each analysis includes:

- Documentation of the chosen pipeline (scraping, parsing, cleaning)
- Clear code blocks explained before and after with markdown
- Optional visualizations (matplotlib)

## Technologies & Libraries Used

- **Python 3.10+**
- `requests` (HTTP requests)
- `BeautifulSoup4` (HTML table scraping)
- `csv` module (for export and parsing)
- `collections.Counter`, `itertools`
- No pandas, no external databases—everything is done in pure Python

For questions, feedback, or collaboration: [www.linkedin.com/in/jairo-nacurena](https://www.linkedin.com/in/jairo-nacurena)
