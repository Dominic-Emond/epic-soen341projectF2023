from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, or_
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
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

meta = MetaData()

#Broker Table(MySQL)
brokers = Table('Broker', meta,
    Column('Id', Integer, primary_key = True),
    Column('First_Name', String),
    Column('Last_Name', String),
    Column('Email_Address', String),
    Column('Username', String),
    Column('Pass', String))

#Broker Class (python)
class Broker(BaseModel):
    First_Name: str
    Last_Name: str
    Email_Address: str
    Username: str
    Password: str

# Delete Broker
@app.delete("/brokers/{broker_id}")
async def delete_broker(broker_id: int):
    try:
        result = connection.execute(brokers.delete().where(brokers.c.Id == broker_id))
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")
    
    return {
        "message": "Broker deleted"
    }


# Get Broker
@app.get("/brokers/{broker_id}")
async def get_broker(broker_id: int):
    try:
        result = connection.execute(brokers.select().where(brokers.c.Id == broker_id))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")
    
    for row in result:
        return {
            "Id": row.Id,
            "First_Name": row.First_Name,
            "Last_Name": row.Last_Name,
            "Email_Address": row.Email_Address,
            "Username": row.Username,
            "Password": row.Pass
        }

# Post Broker
@app.post("/brokers")
async def post_broker(broker: Broker):

    query = brokers.insert().values(
        First_Name = broker.First_Name,
        Last_Name=broker.Last_Name,
        Email_Address=broker.Email_Address,
        Username=broker.Username,
        Pass=broker.Password
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")
    
    return {
        "message": "Broker created",
        "Id": result.lastrowid
    }

# Post Update
@app.put("/brokers/{broker_id}")
async def update_broker(broker_id: int, broker: Broker):
    query = brokers.update().where(brokers.c.Id == broker_id).values(
        First_Name = broker.First_Name,
        Last_Name=broker.Last_Name,
        Email_Address=broker.Email_Address,
        Username=broker.Username,
        Pass=broker.Password
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")
    
    return {
        "message": "Broker updated"
    }


# Search Broker
@app.get("/searchbroker/{name}")
async def get_broker(name: str):
    try:
        result = connection.execute(brokers.select().where(
            or_(
                brokers.c.First_Name.like(f"%{name}%"),
                brokers.c.Last_Name.like(f"%{name}%")
            )))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")
    
    rows = [
            {
                "Id": row.Id,
                "First_Name": row.First_Name,
                "Last_Name": row.Last_Name,
                "Email_Address": row.Email_Address,
                "Username": row.Username,
                "Password": row.Pass
            }
            for row in result
    ]
    
    return rows