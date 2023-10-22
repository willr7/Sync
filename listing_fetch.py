import json
import urllib.request
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from add_to_database import CPUBenchmarks, GPUBenchmarks, GPUListings


load_dotenv()
db_password = os.getenv("DB_PASSWORD")

user = "root"
password = db_password
host = "localhost"
port = 3306
database_name = "sync"

db_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database_name}"

engine = create_engine(db_url)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

gpu_listings_raw = session.query(GPUBenchmarks).all()
gpu_models = [gpu_listing.model for gpu_listing in gpu_listings_raw]

base_url = "https://www.newegg.com/p/pl?d="

def fetch_model_listings(model):
    model_ = model.replace(" ", "+")
    url = base_url + model_
    resp = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})

    try:
        with urllib.request.urlopen(resp) as response:
            html = response.read()
    except Exception as e:
        print(f"Failed to load URL: {url}")
        print(e)
    
    soup = BeautifulSoup(html, 'html.parser')

    if soup.find('span', class_='result-message-error') is not None:
        return None

    soup = soup.find('div', class_='item-info').find('a', class_='item-title')

    if soup is None:
        return None
    else:
        product_page_link = soup["href"]
    
    listing = {}
    listing["link"] = product_page_link

    resp_product = urllib.request.Request(product_page_link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})

    try:
        with urllib.request.urlopen(resp_product) as response:
            html = response.read()
    except Exception as e:
        print(f"Failed to load URL: {url}")
        print(e)
    
    soup = BeautifulSoup(html, 'html.parser')

    price = soup.find('li', class_='price-current').find('strong').text
    listing["price"] = int(price.replace(',', ''))

    return listing

gpu_model_listings = {}

for model in gpu_models[2000:2200]:
    try: 
        model_listing = fetch_model_listings(model)
        if model_listing is not None:
            gpu_model_listing = GPUListings(link=model_listing["link"], model=model, price=model_listing["price"])
            session.add(gpu_model_listing)
            session.commit()
    except Exception as e:
        print(e)

