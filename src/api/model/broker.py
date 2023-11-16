from sqlalchemy import Table, Column, Integer, String, MetaData
from pydantic import BaseModel

meta = MetaData()

# Python and Table Models
brokers_table = Table('Broker', meta,
    Column('Id', Integer, primary_key=True),
    Column('First_Name', String),
    Column('Last_Name', String),
    Column('Email_Address', String),
    Column('Username', String),
    Column('Pass', String))

class BrokerModel(BaseModel):
    First_Name: str
    Last_Name: str
    Email_Address: str
    Username: str
    Pass: str