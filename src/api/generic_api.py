from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, or_
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import os

# Creates API
app = FastAPI()


#Add CORS to enable the front end to reach it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Database
try:
    #Load the URL from the secret variable
    load_dotenv()
    db_url = os.getenv("URL")
    
    engine = create_engine(db_url, echo = True)
    connection = engine.connect()
except Exception as e:
    print(f"Could not connect to database: {e}")

# Use for Broker Table
meta = MetaData()

# Post Method. Insert data to the Database
def create_record(table, data):
    try:
        query = table.insert().values(**data)
        result = connection.execute(query)
        connection.commit()
        return result.lastrowid
    
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

# Get Method. Get the data from the Database
def read_record(table, id):
    try:
        query = table.select().where(table.c.Id == id)
        result = connection.execute(query)
        row = result.first()
        return row._mapping
    
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

# Put Method. Update the data in the Database
def update_record(table, id, data):
    try:
        query = table.update().where(table.c.Id == id).values(**data)
        connection.execute(query)
        connection.commit()
        return
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}") 

# Delete Method. Delete the row with id in the Database
def delete_record(table, id):
    try:
        query = table.delete().where(table.c.Id == id)
        connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}") 

# Generic CRUD Operations!
def create_table_routes(table, model):
    # Create (Post)
    @app.post(f"/{table.name.lower()}")
    async def create_record_route(item: model):
        id = create_record(table, item.dict())
        return {
            "message": f"{table.name} created",
            "Id": id
        }
    
    # Read (Get)
    @app.get(f"/{table.name.lower()}/{{id}}")
    async def read_record_route(id: int):
        record = read_record(table, id)
        return record
    
    # Update (Put)
    @app.put(f"/{table.name.lower()}/{{id}}")
    async def update_record_route(id: int, item: model):
        update_record(table, id, item.dict())
        return { "message": f"{table.name} updated" }
    
    # Delete
    @app.delete(f"/{table.name.lower()}/{{id}}")
    async def delete_record_route(id: int):
        delete_record(table, id)
        return { "message": f"{table.name} deleted" }

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

# Create the routes
create_table_routes(brokers_table, BrokerModel)