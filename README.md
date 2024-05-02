# WTO News and Events Archive Crawler

This repository contains a crawler designed to retrieve all archives from the [WTO News and Events](https://www.wto.org/english/news_e/news_e.htm) section. The scripts utilize the Selenium Python package to scrape the website. The data, including articles and their details, is stored in JSON format for easy access and manipulation.

## Crawler Workflow

The crawler operates in the following steps:

1. **Retrieving Submenu URLs**: Execute `get_submenu_url.py` to collect all submenu URLs under the Archives section (target menu). This script generates a JSON file named `targetMenuUrlDict.json`, which serves as a reference for subsequent steps.

2. **Collecting Article URLs**: Run `get_article_url.py` to gather URLs for each article listed under each submenu. For each submenu, the URLs will be saved in a CSV file in the path `f'../WTO_data_article/{menuPathName}'`.

3. **Extracting Article Details**: Use `get_article_content.py` to scrape and retrieve details from each individual article. If the article is successfully crawled, it will be saved in a JSON file named `all_article_content.json`, otherwise it is logged as a failed recorded in `fail_record.json`. 

4. **Date Correction**: Use `correct_date.ipynb` to adjust any discrepancies in dates. Modify the code if you find other patterns for data cleansing. Please note that this repository currently does not offer functionality for label correction.

In the end `all_article_content.json` includes `title`, `raw_date`, `raw_label`, `abstract`, `content`, `outboundLinks`, `outboundLinksText`, and `date` under each `url`.
