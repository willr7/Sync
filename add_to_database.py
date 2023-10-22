import sqlalchemy
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
import json

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

base = declarative_base()

user = "root"
password = db_password
host = "localhost"
port = 3306
database_name = "sync"

db_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database_name}"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

class CPUBenchmarks(declarative_base()):
    __tablename__ = "CPU Benchmarks"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    benchmark = sqlalchemy.Column(sqlalchemy.INT)

class GPUBenchmarks(declarative_base()):
    __tablename__ = "GPU Benchmarks"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    benchmark = sqlalchemy.Column(sqlalchemy.INT)

class CPUListings(declarative_base()):
    __tablename__ = "GPU Listings"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    chipset = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    wattage = sqlalchemy.Column(sqlalchemy.INT)
    price = sqlalchemy.Column(sqlalchemy.INT)

class GPUListings(declarative_base()):
    __tablename__ = "GPU Listings"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    wattage = sqlalchemy.Column(sqlalchemy.INT)
    price = sqlalchemy.Column(sqlalchemy.INT)

class MotherboardListings(declarative_base()):
    __tablename__ = "Motherboard Listings"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    chipset = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    price = sqlalchemy.Column(sqlalchemy.INT)

class PowerSupplyListings(declarative_base()):
    __tablename__ = "Power Supply Listings"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    wattage = sqlalchemy.Column(sqlalchemy.INT)
    price = sqlalchemy.Column(sqlalchemy.INT)

def add_cpu_benchmarks(filepath):
    """
    model: VARCHAR
    benchmark: INT

    A dictionary which maps the model to the benchmark
    """
    cpu_benchmarks = []

    with open(filepath, 'r') as f:
        cpu_benchmark_data = json.load(f)

    for key in cpu_benchmark_data.keys():
        model = key
        benchmark = cpu_benchmark_data[key]
        cpu_benchmarks.append(CPUBenchmarks(model=model, benchmark=benchmark))

    session.bulk_save_objects(cpu_benchmarks)
    session.commit()

def add_gpu_benchmarks(filepath):
    """
    model: VARCHAR
    benchmark: INT

    A dictionary which maps the model to the benchmark
    """
    gpu_benchmarks = []

    with open(filepath, 'r') as f:
        gpu_benchmark_data = json.load(f)

    for key in gpu_benchmark_data.keys():
        model = key
        benchmark = gpu_benchmark_data[key]
        gpu_benchmarks.append(GPUBenchmarks(model=model, benchmark=benchmark))

    session.bulk_save_objects(gpu_benchmarks)
    session.commit()

def add_cpu_listings(filepath):
    """
    link: VARCHAR
    model: VARCHAR
    chipset: VARCHAR
    wattage: INT
    price: INT

    A dictionary which maps the model to a dictionary which stores the other fields
    """
    cpu_listings = []

    with open(filepath, 'r') as f:
        cpu_listing_data = json.load(f)
    
    for key in cpu_listing_data.keys():
        model = key
        link = cpu_listing_data[key]["link"]
        chipset = cpu_listing_data[key]["chipset"]
        wattage = cpu_listing_data[key]["wattage"]
        price = cpu_listing_data[key]["price"]
        cpu_listings.append(CPUListings(model=model, link=link, chipset=chipset, wattage=wattage, price=price))
    
    session.bulk_save_objects(cpu_listings)
    session.commit()

def add_gpu_listings(filepath):
    """
    link: VARCHAR
    model: VARCHAR
    wattage: INT
    price: INT

    A dictionary which maps the model to a dictionary which stores the other fields
    """
    gpu_listings = []

    with open(filepath, 'r') as f:
        gpu_listing_data = json.load(f)
    
    for key in gpu_listing_data.keys():
        model = key
        link = gpu_listing_data[key]["link"]
        wattage = gpu_listing_data[key]["wattage"]
        price = gpu_listing_data[key]["price"]
        gpu_listings.append(GPUListings(model=model, link=link, wattage=wattage, price=price))
    
    session.bulk_save_objects(gpu_listings)
    session.commit()

def add_motherboard_listings(filepath):
    """
    model: VARCHAR
    link: VARCHAR
    chipset: VARCHAR
    price: INT

    A dictionary which maps the model to a dictionary which stores the other fields
    """
    motherboard_listings = []

    with open(filepath, 'r') as f:
        motherboard_listing_data = json.load(f)
    
    for key in motherboard_listing_data.keys():
        model = key
        link = motherboard_listing_data[key]["link"]
        chipset = motherboard_listing_data[key]["chipset"]
        price = motherboard_listing_data[key]["price"]
        motherboard_listings.append(GPUListings(model=model, link=link, chipset=chipset, price=price))
    
    session.bulk_save_objects(motherboard_listings)
    session.commit()

def add_power_supply_listings(filepath):
    """
    link: VARCHAR
    model: VARCHAR
    wattage: INT
    price: INT

    A dictionary which maps the model to a dictionary which stores all of the values
    """
    power_supply_listings = []

    with open(filepath, 'r') as f:
        power_supply_data = json.load(f)
    
    for key in power_supply_data.keys():
        model = key
        link = power_supply_data[key]["link"]
        wattage = power_supply_data[key]["wattage"]
        price = power_supply_data[key]["price"]
        power_supply_listings.append(PowerSupplyListings(model=model, wattage=wattage, price=price, link=link))
    
    session.bulk_save_objects(power_supply_listings)
    session.commit()

        
if __name__ == "__main__":
    add_gpu_benchmarks("formatted_gpu_benchmarks.json")
    add_cpu_benchmarks("formatted_cpu_benchmarks.json")