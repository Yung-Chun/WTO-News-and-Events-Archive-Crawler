# WTO News and Events Archive Crawler

This repository contains a crawler designed to retrieve all archives from the [WTO News and Events](https://www.wto.org/english/news_e/news_e.htm) section. The scripts utilize the Selenium Python package to scrape the website. The data, including articles and their details, is stored in CSV format for easy access and manipulation.

## Crawler Workflow

The crawler operates in the following steps:

1. **Retrieving Submenu URLs**: Execute `get_submenu_url.py` to collect all submenu URLs under the Archives section. This script generates a JSON file named `targetMenuUrlDict.json`, which serves as a reference for subsequent steps.

2. **Collecting Article URLs**: Run `get_article_url.py` to gather URLs for each article listed under each submenu.

3. **Extracting Article Details**: Use `get_article_content.py` to scrape and retrieve details from each individual article.

4. **Date Correction**: Apply `correct_date.ipynb` for adjusting any discrepancies in dates. Please note that this repository currently does not offer functionality for label correction.
