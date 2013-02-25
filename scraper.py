import requests
from bs4 import BeautifulSoup
import re
from sqlalchemy import create_engine, MetaData, Table
from datetime import datetime

# main url
ROOT_URL = "http://www.apa.sk/index.php?navID=206"

# create engine
engine = create_engine("postgresql://postgres:postgres@localhost/sandbox")
metadata = MetaData(bind=engine)
recipients = Table("recipients", metadata, autoload=True)

# scrape available years
def scrape_years():
    responce = requests.get(ROOT_URL)
    soup = BeautifulSoup(responce.text)
    return [year.text for year in soup.find("select", attrs={"name" : "rok"}).findAll("option", attrs={"value" : re.compile('[0-9]+')})]

# scrape table based on year and page
def scrape_table(year, page):
    responce = requests.get(ROOT_URL + "&rok=" + year + "&offset=" + "%s" % (page))
    soup = BeautifulSoup(responce.text)
    return soup.find("table").findAll("tr")[1:]

# load partional table
def load_table(table, year):
    for row in table:
        cells = row.findAll("td")
        record = {
            "source_EU": cells[0].text,
            "source_SK": cells[1].text,
            "paid_amount": cells[2].text,
            "currency": cells[3].text,
            "fund": cells[4].text,
            "beneficiary": cells[5].text,
            "zip": cells[6].text,
            "city": cells[7].text,
            "year": year
        }
        recipients.insert().execute(record)

# scrape pagecnt per year
def scrape_pagecnt_per_year(year):
    responce = requests.get(ROOT_URL + "&rok=" + year)
    soup = BeautifulSoup(responce.text)
    
    lastpage = soup.find("div", id="strankovanie").findAll("a")[-1]
    match = re.search(r"offset=(?P<lastpage>[0-9]+)", lastpage["href"])
    return int(match.group("lastpage")) + 1

# scrape and load data
def scrape_and_load():
    for year in scrape_years():
        pagecnt = scrape_pagecnt_per_year(year)
        for page in range(pagecnt):
            table = scrape_table(year, page)
            load_table(table, year)

if __name__ == "__main__":
    scrape_and_load()