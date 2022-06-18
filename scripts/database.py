import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import create_engine, MetaData, Table
import pandas as pd

db_string = "postgresql://admin:123@127.0.0.1:5432/spotify"

engine = create_engine(db_string)
Base = declarative_base()
metadata = MetaData()

table = Table("testTable", metadata , autoload=True, autoload_with=engine)

print(engine.table_names())
print(repr(table))
print(table.columns.keys())

#with open("data/data.csv",'r',encoding='Latin1') as file:
df = pd.read_csv("data/charts.csv")
print(df.head())