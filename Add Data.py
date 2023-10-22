import sqlalchemy
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import declarative_base
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

class CPUBenchmarks(declarative_base()):
    __tablename__ = "CPU Benchmarks"

    id = sqlalchemy.Column(sqlalchemy.BIGINT, autoincrement=True, primary_key=True)
    model = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    benchmark = sqlalchemy.Column(sqlalchemy.INT)
    originalprice = sqlalchemy.Column(sqlalchemy.DOUBLE)

cpu_benchmarks = []

insert_statement = insert(CPUBenchmarks).values(model="Intel Core i9-13900K", benchmark=100, originalprice=589)

with engine.connect() as connection:
    connection.execute(insert_statement)
    connection.commit()