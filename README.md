# Tour de France Data Science Project

## 📖 Project Overview

This project explores the rich history of the **Tour de France** cycling race by extracting structured data from Wikipedia and performing insightful analyses. It covers:

- Scraping detailed data of winners, multiple champions, race lengths, and ages  
- Cleaning and saving this data into reproducible **CSV, JSON, and Pickle** formats  
- Analyzing key research questions with **Python, NumPy, and Matplotlib**  
- Visualizing findings using clear charts to reveal trends and remarkable records  

---

## 📂 Datasets

The cleaned datasets are saved in the `data/` folder:

- **tdf_winner_nationalities_clean.csv**  
  Summary of unique winners per country, extracted from the “By nationality” table.  

- **tdf_multiple_winners_clean.json**  
  Details of cyclists with more than three Tour wins, including years and Wikipedia links.  

- **tdf_shortest_tour_clean.p**  
  Data of each Tour’s length (in km) and winning time, excluding invalid or disputed years.  

- **tdf_winner_ages_clean.csv**  
  Age of each Tour winner when victorious, obtained by combining personal birthdates with winning years.  

---

## ❓ Key Research Questions

1. **Which nationality has the most unique Tour de France winners?**  
   → Analyzed by counting winners per country and visualizing with a bar chart.  

2. **Which cyclists have won the Tour more than three times, and in which years?**  
   → Presented detailed timelines of multiple Tour winners using structured JSON data and a horizontal bar chart.  

3. **How long was the shortest Tour de France (in days and kilometers)?**  
   → Examined shortest editions by distance and time, shown with scatter plots for historical trends.  

4. **How do the winning times of the five-time Tour de France champions compare?**  
   → Compared winning times as grouped bar charts to reflect performance across multiple victories.  

5. **At what age do Tour de France winners achieve victory?**  
   → Visualized winner ages over history with scatter plots revealing no fixed winning age but a range of champion profiles.  

---

## 🛠️ Technologies & Libraries

- Python 3.x  
- **Requests** & **BeautifulSoup** for web scraping  
- **CSV, JSON, Pickle** for data storage and interoperability  
- **NumPy & Matplotlib** for numerical analysis and visualization  
- Robust **regular expressions** for precise data extraction  

---

## ▶️ How to Run

1. Scrape & clean data via the Jupyter notebook **01_scraping_cleaning.ipynb**  
2. Perform analyses and generate plots with **02_analysis.ipynb**  
3. Explore individual question notebooks or extend with your own research  

---

## 🎯 Project Goals

- Demonstrate robust data scraping and munging techniques  
- Practice Pythonic data analysis workflows  
- Develop insightful visualizations aligned with research questions  
- Enable reproducible, shareable results for learning and collaboration  

---

## 🚀 Future Work

- Extend analysis to other cycling Grand Tours (Giro d’Italia, Vuelta a España)  
- Incorporate stage-level data for deeper performance insights  
- Explore team dynamics and strategies across different eras  
- Add interactive dashboards for richer exploration of Tour de France history  
