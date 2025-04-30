from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

# === CONFIGURATION ===
search = "Men jeans"   # Change this to your keyword
limit = 0        # 0 = scrape all products


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)


search_url = f"https://www.bewakoof.com/search?q={search}"
driver.get(search_url)


scroll_pause = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


soup = BeautifulSoup(driver.page_source, "html.parser")
product_base = "https://www.bewakoof.com"
product_links = []

for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    if href.startswith("/p/"):
        full_url = product_base + href
        if full_url not in product_links:
            product_links.append(full_url)

print(f"Found {len(product_links)} products for the searched item")


if limit > 0:
    product_links = product_links[:limit]

# === Scrape each product ===
product_data = []

for link in product_links:
    print(f"Scraping: {link}")
    driver.get(link)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Default values
    name = price = rating = rated_count = review_count = "N/A"

    # --- Extract name and price from embedded JSON ---
    try:
        script_tag = soup.find("script", id="__NEXT_DATA__")
        if script_tag:
            json_data = json.loads(script_tag.string)
            product_json = json_data["props"]["pageProps"]["productDetails"]
            name = product_json.get("name", "N/A")
            price = product_json.get("price", "N/A")
    except Exception as e:
        print("Failed to extract product JSON:", e)

    # --- Extract rating ---
    try:
        rating_spans = soup.find_all("span", class_="sc-f48c17b3-0")
        for span in rating_spans:
            text = span.get_text(strip=True)
            if text.replace('.', '', 1).isdigit():
                rating = text
                break
    except Exception as e:
        print("Rating parse failed:", e)

    try:
        info_spans = soup.find_all("span", class_="sc-f48c17b3-0")
        for span in info_spans:
            text = span.get_text(strip=True).lower()
            if "ratings" in text and rated_count == "N/A":
                rated_count = text
            elif "reviews" in text and review_count == "N/A":
                review_count = text
    except Exception as e:
        print("Rating count/review count parse failed:", e)

    product_data.append({
        "product_name": name,
        "price": price,
        "rating": rating,
        "number_of_reviews": review_count,
        "product_url": link
    })

driver.quit()

# === Save results to CSV ===
df = pd.DataFrame(product_data)
csv_name = f"bewakoof_{search}_products.csv"
df.to_csv(csv_name, index=False)
print(f"Scraping complete. Data saved to '{csv_name}'")
