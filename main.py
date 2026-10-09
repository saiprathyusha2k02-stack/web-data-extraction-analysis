
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
OUTPUT_FILE = "scraped_books.csv"

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_books(max_pages=3):
    all_books = []

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BeginnerResearchProject/1.0)"
    }

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping page {page}: {url}")

        try:
            response = requests.get(
                url, headers=headers, timeout=20
            )
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"Could not retrieve page {page}: {error}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")

        for product in products:
            title_tag = product.select_one("h3 a")
            price_tag = product.select_one(".price_color")
            stock_tag = product.select_one(".availability")
            rating_tag = product.select_one(".star-rating")

            if not title_tag or not price_tag:
                continue

            rating_word = ""
            rating_value = None

            if rating_tag:
                classes = rating_tag.get("class", [])
                rating_word = next(
                    (word for word in classes
                     if word in rating_map),
                    ""
                )
                rating_value = rating_map.get(rating_word)

            price_text = price_tag.get_text(strip=True)
            price_text = price_text.replace("Â", "")

            try:
                price = float(
                    price_text.replace("£", "").replace("Â", "")
                )
            except ValueError:
                price = None

            availability = (
                stock_tag.get_text(" ", strip=True)
                if stock_tag else "Unknown"
            )

            all_books.append({
                "Title": title_tag.get("title", title_tag.get_text(strip=True)),
                "Price_GBP": price,
                "Rating": rating_value,
                "Availability": " ".join(availability.split()),
                "Source_Page": page
            })

        time.sleep(0.5)

    return pd.DataFrame(all_books)


def analyze_data(df):
    if df.empty:
        print("No data collected. Please check the website connection.")
        return

    # Clean and organize the data
    df = df.drop_duplicates(subset=["Title"])
    df["Price_GBP"] = pd.to_numeric(
        df["Price_GBP"], errors="coerce"
    )
    df["Rating"] = pd.to_numeric(
        df["Rating"], errors="coerce"
    )
    df = df.dropna(subset=["Title", "Price_GBP"])
    df = df.reset_index(drop=True)

    # Export the cleaned dataset
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("\n--- DATASET OVERVIEW ---")
    print(f"Total books collected: {len(df)}")
    print(f"Missing values:\n{df.isnull().sum()}")

    print("\n--- PRICE ANALYSIS ---")
    print(f"Average price: £{df['Price_GBP'].mean():.2f}")
    print(f"Minimum price: £{df['Price_GBP'].min():.2f}")
    print(f"Maximum price: £{df['Price_GBP'].max():.2f}")
    print(f"Median price: £{df['Price_GBP'].median():.2f}")

    cheapest = df.loc[df["Price_GBP"].idxmin()]
    expensive = df.loc[df["Price_GBP"].idxmax()]

    print(f"\nCheapest book: {cheapest['Title']}")
    print(f"Cheapest price: £{cheapest['Price_GBP']:.2f}")
    print(f"Most expensive book: {expensive['Title']}")
    print(f"Most expensive price: £{expensive['Price_GBP']:.2f}")

    print("\n--- RATING ANALYSIS ---")
    print(f"Average rating: {df['Rating'].mean():.2f} / 5")

    print("\nBooks by rating:")
    print(df["Rating"].value_counts().sort_index())

    print("\n--- AVAILABILITY ANALYSIS ---")
    print(df["Availability"].value_counts())

    print("\n--- SAMPLE DATA ---")
    print(df.head(10).to_string(index=False))

    print(f"\nCleaned dataset saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    data = scrape_books(max_pages=3)

    if not data.empty:
        analyze_data(data)
    else:
        print("No books were scraped. Check the connection and try again.")