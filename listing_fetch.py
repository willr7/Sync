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
    url = base_url + "&Order=1"
    resp = urllib.request.Request(url)

    with urllib.request.urlopen(resp) as response:
        html = response.read()
    
    

for model in cpu_models:
    fetch_model_listings(model)