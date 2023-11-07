import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
import json
from random import randrange

class GPUTable(declarative_base()):
    __tablename__ = 'GPU Table'

    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255), primary_key=True)
    benchmark = sqlalchemy.Column(sqlalchemy.INT)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    price = sqlalchemy.Column(sqlalchemy.INT)

class CPUTable(declarative_base()):
    __tablename__ = 'CPU Table'

    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255), primary_key=True)
    benchmark = sqlalchemy.Column(sqlalchemy.INT)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    price = sqlalchemy.Column(sqlalchemy.INT)

"""
take in a cpu score and a gpu score
return cpu parts

CPU: sql
GPU: sql
Power Supply: json
motherboard: json
case: json
ram: json
"""

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

with open('cases.json', 'r') as f:
    cases_data = json.load(f)
    cases_names = list(cases_data)

with open('mother.json', 'r') as f:
    mother_data = json.load(f)
    mother_names = list(mother_data)

with open('power.json', 'r') as f:
    power_data = json.load(f)
    power_names = list(power_data)

with open('RAM.json', 'r') as f:
    ram_data = json.load(f)
    ram_names = list(ram_data)

case = cases_names[randrange(0, len(cases_names))]
mother = mother_names[randrange(0, len(mother_names))]
power = power_names[randrange(0, len(power_names))]
ram = ram_names[randrange(0, len(ram_names))]


def build_pc(cpu_score, gpu_score):
    """
    returns a dictionary which maps the part name to a list
    where the first element of the list is the name
    The second element of the list is the price
    and the third element is a link to buy the product
    """
    gpu_results = session.query(GPUTable).filter(GPUTable.benchmark >= gpu_score).limit(10).all()
    gpu_dict = {}
    min_gpu_price = 10000000
    cheapest_gpu = ""
    
    for result in gpu_results:
        if min_gpu_price > result.price:
            min_gpu_price = result.price
            cheapest_gpu = result.model
            min_gpu_link = result.link
        gpu_dict[result.model] = [result.price, result.link]

    cpu_results = session.query(CPUTable).filter(CPUTable.benchmark >= cpu_score).limit(10).all()
    cpu_dict = {}
    min_cpu_price = 10000000
    cheapest_cpu = ""
    
    for result in cpu_results:
        if min_cpu_price > result.price:
            min_cpu_price = result.price
            cheapest_cpu = result.model
            min_cpu_link = result.link
        cpu_dict[result.model] = [result.price, result.link]
    
    build = {
        "case": [],
        "mother": [],
        "power": [],
        "ram": [],
        "gpu": [],
        "cpu": []
    }

    build["case"].append(case)
    build["case"].append(cases_data[case]["price"])
    build["case"].append(cases_data[case]["link"])

    build["mother"].append(mother)
    build["mother"].append(mother_data[mother]["price"])
    build["mother"].append(mother_data[mother]["link"])

    build["power"].append(power)
    build["power"].append(power_data[power]["price"])
    build["power"].append(power_data[power]["link"])

    build["ram"].append(ram)
    build["ram"].append(ram_data[ram]["price"])
    build["ram"].append(ram_data[ram]["link"])

    build["gpu"].append(cheapest_gpu)
    build["gpu"].append(min_gpu_price)
    build["gpu"].append(min_gpu_link)

    build["cpu"].append(cheapest_cpu)
    build["cpu"].append(min_cpu_price)
    build["cpu"].append(min_cpu_link)
    
    return build

if __name__ == "__main__":
    print(build_pc(500, 500))