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
    originalprice = sqlalchemy.Column(sqlalchemy.DOUBLE)

class GPUBenchmarks(declarative_base()):
    __tablename__ = "GPU Benchmarks"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    benchmark = sqlalchemy.Column(sqlalchemy.INT)
    originalprice = sqlalchemy.Column(sqlalchemy.DOUBLE)

def add_cpu_benchmarks(filepath):
    cpu_benchmarks = []

    with open(filepath, 'r') as f:
        cpu_benchmark_data = json.load(f)

    for key in cpu_benchmark_data.keys():
        model = key
        benchmark = cpu_benchmark_data[key][0]
        originalprice = cpu_benchmark_data[key][1]
        print(originalprice)
        if originalprice == 'NA':
            originalprice = None
        cpu_benchmarks.append(CPUBenchmarks(model=model, benchmark=benchmark, originalprice=originalprice))

    session.bulk_save_objects(cpu_benchmarks)
    session.commit()

def add_gpu_benchmarks(filepath):
    gpu_benchmarks = []

    with open(filepath, 'r') as f:
        gpu_benchmark_data = json.load(f)

    for key in gpu_benchmark_data.keys():
        model = key
        benchmark = gpu_benchmark_data[key][0]
        originalprice = gpu_benchmark_data[key][1]
        if originalprice == 'NA':
            originalprice = None
        gpu_benchmarks.append(GPUBenchmarks(model=model, benchmark=benchmark, originalprice=originalprice))

    session.bulk_save_objects(gpu_benchmarks)
    session.commit()

if __name__ == "__main__":
    add_gpu_benchmarks("gpu_benchmarks.json")

# with engine.connect() as connection:
#     connection.execute(insert_statement)
#     connection.commit()