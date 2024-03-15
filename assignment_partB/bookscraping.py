import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# connecting to mongodb
client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']
collection = db['bookscrape']

# function to scrape a single page and store data in mongodb
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    # soup.find_all("a", class_="sister")
    # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
    #  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
    #  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    for book in books:
        title = book.h3.a['title']
        price_text = book.find('p', class_='price_color').text  # Keep as string
        availability = book.find('p', class_='instock availability').text.strip()
        rating_classes = book.find('p', class_='star-rating')['class']
        rating = ['One', 'Two', 'Three', 'Four', 'Five'].index(rating_classes[1]) + 1
        # inserting data into mongodb
        collection.insert_one({
            'title': title,
            'price': price_text,
            'availability': availability,
            'rating': rating
        })

# function to scrape all pages
def scrape_all_pages():
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    for page in range(1, 51):  # 50 pages
        url = base_url.format(page)
        print("Scraping page", page)  # printing progress message
        scrape_page(url)
    print("Scraping complete!")  # print completion message

# function call
scrape_all_pages()

# closing the mongodb connection
client.close()
