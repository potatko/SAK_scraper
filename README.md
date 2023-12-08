# SAK_scraper

Python bot designed to scrape advocate information from "Slovenská advokátska komora".

## Features

- Scrapes advocate details including name, telephone, mobile, and email.
- Navigates through multiple pages (pagination support).
- Handles dynamic content loading using Selenium WebDriver.
- Exports the scraped data to a CSV file with appropriate formatting.
- Implements error handling to manage web elements that change after page navigation.

## Technologies

- Python
- Selenium WebDriver
- CSV module for data export

## Setup and Usage

1. Requires Python and Selenium WebDriver.
2. Install dependencies from `requirements.txt`.
3. Run the script to start scraping. The data will be saved in `advocate_details.csv`.

## Note

This bot uses full XPath for scraping some information and might not work in the future if the website's structure changes.
