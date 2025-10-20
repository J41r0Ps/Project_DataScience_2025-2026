# 🚴 Tour de France Data Science Project

## Introduction

This project demonstrates an end-to-end data science workflow focused on the multi-stage cycling event, Tour de France. The goal is to gain hands-on experience with web scraping, data cleaning, Pythonic analysis, and communicating results clearly—skills that are essential for roles such as data scientist, analyst, or engineer.

All data is collected via web scraping (using BeautifulSoup) from public HTML tables on Wikipedia. All data processing is done without pandas—using only Python's built-in tools, list comprehensions, and modules such as `collections` and `csv`.

## Objectives

- Demonstrate complete data science skills: from scraping real websites to analytical insights
- Explore historical Tour de France statistics and trends
- Emphasize Pythonic code (clear, efficient, idiomatic Python)
- Document every method and choice for easy understanding and reproducibility
- Communicate findings in a way that is accessible for both technical and non-technical audiences

## Data

**Source:**  
Wikipedia – List of Tour de France general classification winners

**Method:**  
Relevant tables are scraped directly from the HTML using BeautifulSoup. The data is cleaned (handling missing values, type conversions, deduplication) and exported as CSV for later analysis.

## Project Structure

```
├── README.md
├── 01_scraping_cleaning.ipynb       # Web scraping and data
├── 02_analysis.ipynb                # Data analysis & answering the
├── data/
│   ├── ...
├── .gitignore
```

## Research Questions & Methods

This project answers the following five questions, chosen for their data richness and the challenge in collecting and processing them from live websites:

1. **Which nationality has the most unique Tour de France winners?**  
   Analyze the “By nationality” table. Count unique cyclists per country.

2. **Which cyclists have won the Tour more than twice, and in which years?**  
   Scrape the “Multiple winners” table. List cyclists, their win counts, and years.

3. **How long was the shortest Tour de France (in days and kilometers)?**  
   Parse the main winners’ history table. Extract the distance and compute/min search.

4. **What is the average speed (km/h) across all Tour wins by Jacques Anquetil?**  
   For each of Anquetil’s winning years, follow table links, extract distance and time, calculate speed, and average across all his wins.

5. **Which multiple-time winner spent the most total hours in yellow (total GC winning time in all winning years)?**  
   For each multi-winner, use year links to extract winning time from each page, sum for each cyclist.

Each research question is documented with:

- Exact table(s) or Wikipedia subpages used
- Pipeline documentation (scraping, cleaning, aggregation)
- Clean and clear Python code (with markdown explanation before and after)
- Short conclusion or visualization

## Technologies & Libraries Used

- Python 3.10+
- `requests`
- `BeautifulSoup4`
- `csv`
- `collections.Counter`, `itertools`
- No pandas, no external databases

---

For questions, feedback, or collaboration: [www.linkedin.com/in/jairo-nacurena](https://www.linkedin.com/in/jairo-nacurena)
