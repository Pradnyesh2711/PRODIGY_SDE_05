from bs4 import BeautifulSoup
import requests
import psycopg2


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
    CREATE TABLE IF NOT EXISTS articles (
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
    cursor.execute("INSERT INTO articles (title, link) VALUES (%s, %s)", (title, link))
    conn.commit()
    conn.close()
    print(f"Inserted: Title - {title}, Link - {link}")


# Create the articles table
create_table()

response = requests.get("https://en.wikipedia.org/wiki/History_of_India")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

articles = soup.select(".mw-redirect")

article_texts = []
article_links = []
for article in articles:
    article_texts.append(article.getText())
    article_links.append(article.get("href"))

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


# with open("website.html", encoding="utf8") as fs:
#     content = fs.read()

# soup = BeautifulSoup(content, "html.parser")  # May not work for some websites
# soup = BeautifulSoup(content, "lxml")
# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)
# print(soup)
# print(soup.prettify())
# print(soup.p)
# print(soup.a)

# all_anchor_tags = soup.find_all(name="a")

# for tag in all_anchor_tags:
#     print(tag.get("href"))

# heading = soup.find(name="h1", id="name")
# print(heading)
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading)

# company_url = soup.select_one(selector="p a")
# print(company_url)


