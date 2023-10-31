from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

# Creates API
app = FastAPI()

# Connect to Database
try:
    engine = create_engine('Insert here', echo = True)
    connection = engine.connect()
except:
    print("Could not connect to database")

meta = MetaData()
brokers = Table('Broker', meta,
    Column('Id', Integer, primary_key = True),
    Column('First_Name', String),
    Column('Last_Name', String),
    Column('Email_Address', String),
    Column('Username', String),
    Column('Pass', String))

# Get Broker
@app.get("/brokers/{broker_id}")
async def get_broker(broker_id: int):
    try:
        result = connection.execute(brokers.select().where(brokers.c.Id == broker_id))
    except:
        raise HTTPException(status_code=404, detail="Invalid Query")
    
    for row in result:
        print(row)
        return {
            "Id": row.Id,
            "First_Name": row.First_Name,
            "Last_Name": row.Last_Name,
            "Email_Address": row.Email_Address,
            "Username": row.Username,
            "Password": row.Pass
        }