import json
import urllib.request
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from add_to_database import CPUBenchmarks, GPUBenchmarks

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

cpu_listings_raw = session.query(GPUBenchmarks).all()
cpu_models = [cpu_listing.model.replace(" ", "+") for cpu_listing in cpu_listings_raw]

base_url = "https://www.newegg.com/p/pl?d="

def fetch_model_listings(model):
    url = base_url + model
    resp = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(resp) as response:
            html = response.read()
    except Exception as e:
        print(f"Failed to load URL: {url}")
        print(e)
    
    soup = BeautifulSoup(html, 'html.parser')

    soup = soup.find('div', class_='item-info').find('a', class_='item-title')

    if soup is None:
        print(f"could not find product page: {model}")
    else:
        product_page_link = soup["href"]
        print(product_page_link)

for model in cpu_models:
    fetch_model_listings(model)