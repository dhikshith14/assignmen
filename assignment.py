Python 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime

# Define the URL to scrape
url = 'https://www.theverge.com/'

# Make a GET request to the URL and extract the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the articles on the page
articles = soup.find_all('article')

# Define the CSV and SQLite database file names
date = datetime.datetime.now().strftime("%d%m%Y")
csv_filename = f'{date}_verge.csv'
sqlite_filename = f'{date}_verge.sqlite'

# Connect to the SQLite database and create a table for the data
conn = sqlite3.connect(sqlite_filename)
c = conn.cursor()
c.execute('''CREATE TABLE articles
             (id INTEGER PRIMARY KEY,
              url TEXT,
              headline TEXT,
              author TEXT,
              date TEXT)''')

# Loop through each article and extract the data
for i, article in enumerate(articles):
    # Extract the headline and URL
    headline = article.h2.a.text.strip()
    url = article.h2.a['href']

    # Extract the author and date
    author = article.find('span', {'class': 'c-byline__author-name'}).text.strip()
    date = article.find('time')['datetime'].split('T')[0]

    # Write the data to the CSV file
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i+1, url, headline, author, date])

    # Write the data to the SQLite database
    c.execute(f"INSERT INTO articles VALUES ({i+1}, '{url}', '{headline}', '{author}', '{date}')")

# Commit the changes and close the SQLite connection
conn.commit()
conn.close()