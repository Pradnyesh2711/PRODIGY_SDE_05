from bs4 import BeautifulSoup
import requests
import psycopg2
from lxml import etree


# Function to create a PostgreSQL connection
def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="wiki_data",
        user="postgres",
        password="chaitya"
    )


# Function to create the articles table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS path_link (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        link TEXT
    )
    """)
    conn.commit()
    conn.close()


# Function to insert data into the articles table
def insert_data(title, link):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO path_link (title, link) VALUES (%s, %s)", (title, link))
    conn.commit()
    conn.close()
    print(f"Inserted: Title - {title}, Link - {link}")


# Create the articles table
create_table()

response = requests.get("https://en.wikipedia.org/wiki/History_of_India")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

# Use lxml to create an ElementTree from the BeautifulSoup object
root = etree.HTML(str(soup))

# Modify the XPath expressions to select the elements you want
article_texts = root.xpath('//a[@class="mw-redirect"]/text()')
article_links = root.xpath('//a[@class="mw-redirect"]/@href')

# Insert data into the articles table
for title, link in zip(article_texts, article_links):
    insert_data(title, link)

# Fetch and print data from the articles table
conn = create_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM articles")
rows = cursor.fetchall()
for row in rows:
    print("Title:", row[1])
    print("Link:", row[2])
    print("\n")
conn.close()
