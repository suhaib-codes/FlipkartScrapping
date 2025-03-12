# FlipkartScrapping


## Overview

This Python script scrapes product details of shoes from Flipkart and saves the extracted data into a CSV file. The script uses **BeautifulSoup** for web scraping and **pandas** for data storage.

## Features

- Extracts product details including:
  - Product Name
  - Company Name
  - Price
  - Rating
  - Number of Reviews
  - Product Link
- Saves data into a CSV file (`flipkart_shoes.csv`).
- Supports scraping multiple pages (configurable).
- Filters data to display only Puma shoes in a separate output.

## Requirements

Ensure you have the following Python libraries installed:

```sh
pip install requests beautifulsoup4 pandas
```

## Usage

1. Clone or download this repository.
2. Run the script using:
   ```sh
   python script.py
   ```
3. The extracted data will be saved in `flipkart_shoes.csv`.

## Output

The repository contains two output files:

1. **output\_Flipkart\_shoes\_data.csv** - Displays all scraped shoe products.
2. **output\_Puma\_shoes.csv** - Displays only Puma-branded shoes (with some other sponsored products).




