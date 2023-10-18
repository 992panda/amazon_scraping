import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import json
from unidecode import unidecode
import mysql.connector
# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "zoro",
    "password": "",
    "database": "product_data"
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Alt-Used': 'www.amazon.de',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'www.amazon.de',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'TE': 'trailers',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'
}

def read_csv(filename='Amazon Scraping - Sheet1.csv'):
    asins = []
    countries = []
    with open(filename, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',')
        for row in csv_reader:
            asin = row['Asin']
            country = row['country']
            asins.append(asin)
            countries.append(country)
    return asins, countries

def scrape_product_data(asin, country):
    url = f"https://www.amazon.{country}/dp/{asin}"
    response = requests.get(url, headers=headers)
    product_data = {
        'title': None,
        'url': url, 
        'image_sources': [],
        'price': None,
        'details': []
    }
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_data['title'] = soup.title.text
        img_wrappers = soup.select('div.imgTagWrapper img')#product image
        product_data['image_sources'] = [img.get('src') for img in img_wrappers]
        price_element = soup.find(class_='a-offscreen') # product price
        if price_element: 
            product_data['price'] = unidecode(price_element.text.strip()) #unidecode is used to decode unicode charcacters
        prod_details = soup.select('#detailBullets_feature_div .a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list > li') #product details 
        product_data['details'] = [unidecode(' '.join(li.text.strip().split())) for li in prod_details]
        rating_element = soup.select_one('.a-popover-trigger .a-icon-star .a-icon-alt') #product rating
        if rating_element: 
            rating = unidecode(rating_element.text)
            product_data['details'].append(f'Rating: {rating}')
            
        else:
            product_data['details'].append('rating not found')    

    elif response.status_code == 404:
        print(f"URL {url} returned a 404 error. Skipping...")
        return None  # Return None for 404 errors
    else:
        print(f'Error: Received status code {response.status_code} for {url}.')
        return None     
    return product_data # product data is in dict


def upload_to_mysql(product_data_list):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # MySQL query to insert data into the table
    insert_query = "INSERT INTO scraped_products (title, image_sources, price, details) VALUES (%s, %s, %s, %s)"

    for product_data in product_data_list:
        title = product_data['title']
        image_sources = json.dumps(product_data['image_sources'])
        price = product_data['price']
        details = json.dumps(product_data['details'])
        
        data = (title, image_sources, price, details)
        cursor.execute(insert_query, data)

    connection.commit()
    cursor.close()
    connection.close()



def main():
    asins, countries = read_csv()
    product_data_list = []  #list to store product data which are in dict
    for asin, country in zip(asins, countries): #zpiing list to cosntruct url
        product_data = scrape_product_data(asin, country)
        if product_data is not None:
            product_data_list.append(product_data)
            print(product_data)
            print('-' * 50)
            delay = random.uniform(1, 5)  # Generate a random float between 1 and 5 for delay in request
            print(f"Waiting for {delay:.2f} seconds before the next request...")
            time.sleep(delay)
    with open('output.json', 'w') as jsonfile:  #dumping data in json
        json.dump(product_data_list, jsonfile, indent=4)
    #upload_to_mysql(product_data_list)

    print("Data uploaded to MySQL database.")
    print("Scraping completed. Data saved in 'output.json'.")
    






if __name__ == "__main__":
    main()
