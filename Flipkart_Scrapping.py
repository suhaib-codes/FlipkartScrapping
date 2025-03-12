import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.flipkart.com/search?q=shoes&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="

max_pages = 50 #change the range to how many pages you want 
product_number = 1  
data = []

for page in range(1, max_pages + 1):  
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        continue  
    
    soup = BeautifulSoup(response.text, "html.parser")
    product_containers = soup.find_all("div", class_="cPHDOP col-12-12")

    for container in product_containers:
        product_details = container.find("a", class_="WKTcLC BwBZTg")  
        if not product_details:
            continue
        
        product_link = "https://www.flipkart.com" + product_details["href"]
        company_name = container.find("div", class_="syl9yP")
        price = container.find("div", class_="Nx9bqj")
        
        company_name = company_name.text.strip() if company_name else "N/A"
        price = price.text.strip() if price else "N/A"
        
        product_response = requests.get(product_link, headers=headers)
        rating_value = "No Rating"
        No_of_rating_and_No_of_reviews = "No Reviews"
        
        if product_response.status_code == 200:
            product_soup = BeautifulSoup(product_response.text, "html.parser")
            rating_tag = product_soup.find("div", class_="XQDdHH _1Quie7")
            rating_value = rating_tag.text.strip() if rating_tag else "No Rating"
            No_of_rating = product_soup.find("span", class_="Wphh3N")
            No_reviews = No_of_rating.find("span") if No_of_rating else None
            No_of_rating_and_No_of_reviews = No_reviews.text.strip() if No_reviews else "No Reviews"
        
        data.append([product_number, company_name, product_details['title'], price, rating_value, No_of_rating_and_No_of_reviews, product_link])
        product_number += 1

# Save data to CSV
df = pd.DataFrame(data, columns=["Product Number", "Company", "Details", "Price", "Rating", "Number of Ratings & Reviews", "Link"])
df.to_csv("flipkart_shoes.csv", index=False, encoding="utf-8-sig")

print("Data has been saved to flipkart_shoes.csv")
