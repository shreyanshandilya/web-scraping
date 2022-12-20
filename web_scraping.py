import requests
import selectorlib
import time
import sqlite3

connection = sqlite3.connect(r"C:\Users\Shreyansh Shandilya\OneDrive\Desktop\Web Scraping\data.db")

URL = "http://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    response = requests.get(url)
    source = response.text
    return source

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band,city,date))
    rows = cursor.fetchall()

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file(r"C:\Users\Shreyansh Shandilya\OneDrive\Desktop\Web Scraping\extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

while True:

    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    if extracted != "No upcoming tours":
        row = read(extracted)
        if not row:
            store(extracted)
    time.sleep(2)
