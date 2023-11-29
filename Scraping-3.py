from bs4 import BeautifulSoup
import requests
import pymongo

# Function to create a MongoDB connection and get a reference to the database and collection
def create_connection():
    client = pymongo.MongoClient("mongodb+srv://pradnyesh1008:Pradnyesh@cluster01.ukpogid.mongodb.net/?retryWrites=true&w=majority")
    db = client["cluster01"]  # Create or connect to the "wiki_data" database
    collection = db["articles"]  # Create or connect to the "articles" collection
    return collection

# Function to insert data into the MongoDB collection
def insert_data(title, link, collection):
    data = {"title": title, "link": link}
    collection.insert_one(data)
    print(f"Inserted: Title - {title}, Link - {link}")

# Create a reference to the MongoDB collection
collection = create_connection()

response = requests.get("https://en.wikipedia.org/wiki/Jainism")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

articles = soup.select(".mw-redirect")

article_texts = []
article_links = []
for article in articles:
    article_texts.append(article.getText())
    article_links.append(article.get("href"))

# Insert data into the MongoDB collection
for title, link in zip(article_texts, article_links):
    insert_data(title, link, collection)

# Fetch and print data from the MongoDB collection
articles_data = collection.find()
for article in articles_data:
    print("Title:", article["title"])
    print("Link:", article["link"])
    print("\n")
