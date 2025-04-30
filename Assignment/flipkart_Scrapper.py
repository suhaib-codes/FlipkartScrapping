import requests
from bs4 import BeautifulSoup
import json
import time
import random
import re


class FlipkartScraper:
    def __init__(self, search_query, max_pages=3):
        self.query = search_query.replace(" ", "+")
        self.max_pages = max_pages
        self.base_url = "https://www.flipkart.com/search?q="
        self.product_base_url = "https://www.flipkart.com"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.get_random_user_agent(),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        })
        self.products = []

    def get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
        ]
        return random.choice(user_agents)

    def fetch_page(self, page):
        url = f"{self.base_url}{self.query}&page={page}"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            else:
                print(f"Status code {response.status_code} on page {page}")
        except Exception as e:
            print(f"Exception while fetching page {page}: {e}")
        return None

    def parse_products(self, soup):
        containers = soup.find_all("div", class_="ybB1XH")

        for item in containers:
            title_tag = item.find("div", class_="kv0tEm")
            price_tag = item.find("div", class_="Nx9bqj OQ4U3k")
            rating_tag = item.find("div", class_="XQDdHH")
            review_info_tag = item.find("span", class_="Bz-crL")
            link_tag = item.find("a", href=True)

            if title_tag and price_tag and link_tag:
                name = re.sub(r'^\d+\.\s*', '', title_tag.text.strip())
                price = price_tag.text.strip().replace("₹", "").replace(",", "")
                rating = rating_tag.text.strip() if rating_tag else "N/A"
                product_url = self.product_base_url + link_tag['href'].split('?')[0]

                ratings = reviews = "N/A"
                if review_info_tag:
                    parts = review_info_tag.text.replace(",", "").split("&")
                    try:
                        ratings = parts[0].strip().split()[0]
                        reviews = parts[1].strip().split()[0] if len(parts) > 1 else "N/A"
                    except:
                        pass

                self.products.append({
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "ratings_count": ratings,
                    "reviews_count": reviews,
                    "url": product_url
                })

    def run(self):
        for page in range(1, self.max_pages + 1):
            print(f"Scraping page {page}...")
            soup = self.fetch_page(page)
            if soup:
                self.parse_products(soup)
            time.sleep(random.uniform(2, 5))  
        self.save_to_json()

    def save_to_json(self):
        filename = f"{self.query}_flipkart_data.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.products, f, indent=4, ensure_ascii=False)
        print(f"Scraped data saved to: {filename}")


if __name__ == "__main__":
    scraper = FlipkartScraper("puma shoes", max_pages=100)
    scraper.run()
