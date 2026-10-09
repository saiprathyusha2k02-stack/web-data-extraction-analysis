# web-data-extraction-analysis
Python web scrapping,data cleaning,and exploratory data analysis project

# Web Data Extraction & Analysis

## Project Overview
This project uses Python to collect publicly accessible book
information from a practice website, clean the data, and perform
exploratory data analysis (EDA).

## Objectives
- Extract book titles, prices, ratings, and availability.
- Collect data using Requests and BeautifulSoup.
- Clean and organize the data using Pandas.
- Analyze price statistics and rating distributions.
- Export the cleaned dataset to CSV.

## Tools and Technologies
- Python
- Requests
- BeautifulSoup
- Pandas
- CSV
- GitHub Codespaces

## Data Source
Books to Scrape: https://books.toscrape.com/

This is a practice website intended for web-scraping exercises.

## Project Workflow
1. Send HTTP requests to the website.
2. Parse HTML using BeautifulSoup.
3. Extract structured book information.
4. Clean the data and remove duplicates.
5. Perform exploratory data analysis.
6. Export results to scraped_books.csv.

## Analysis Performed
- Number of books collected
- Missing-value inspection
- Average, minimum, maximum, and median price
- Cheapest and most expensive book
- Average rating and rating distribution
- Availability distribution

## Output
The project generates a cleaned CSV dataset named
scraped_books.csv.

## How to Run
Install the required libraries:

pip install -r requirements.txt

Run the project:

python main.py

## Conclusion
This project demonstrates a basic web-scraping workflow,
data cleaning, structured dataset creation, and exploratory
data analysis using Python.