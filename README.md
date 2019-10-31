# KAP Scraper
KAP (Public Disclosure Platform in English) is an electronic system through which electronically signed notifications required by the capital markets and Borsa Istanbul (Istanbul Stock Market) regulations are publicly disclosed.

This script downloads the latest activity report and financial report of a company from KAP website. The company is specified through a stock code e.g. stock code of "Yapi Kredi Bank" is "YKBNK". Reports are downloaded into a directory called `data`.

## Requirements 
- Python 3.5.5

## Usage 
Install dependencies:
```bash 
$ pip install -r requirements.txt
```

Run the script with a stock code:
```
$ python scraper.py YKBNK 
```

It will download the reports into `data` directory. 

## Current situation
As of October 2019, the scraper may not run correctly since it is not up to date. Anyone interested can contact me via email.
