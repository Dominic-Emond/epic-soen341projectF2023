from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, or_, Boolean
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
try:
    load_dotenv()
    db_url = os.getenv("URL")  # Replace with your actual environment variable name
    engine = create_engine(db_url, echo=True)
    connection = engine.connect()
except Exception as e:
    print(f"Could not connect to database: {e}")

meta = MetaData()

# Client Table
clients = Table(
    'Client', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('First_Name', String, nullable=False),
    Column('Last_Name', String, nullable=False),
    Column('Username', String, nullable=False),
    Column('Password', String, nullable=False),
    Column('Email', String, nullable=False),
    Column('BrokerID', Integer),
    Column('isBroker', Boolean, default=False),
    Column('isClient', Boolean, default=True),  # Set to True for clients
    Column('isSysAdmin', Boolean, default=False)
)

# Client Class (Pydantic model)
class Client(BaseModel):
    First_Name: str
    Last_Name: str
    Username: str
    Password: str
    Email: str
    BrokerID: int = None
    isBroker: bool = False
    isClient: bool = True  # Set to True for clients
    isSysAdmin: bool = False

# CRUD Operations

# Create Client
@app.post("/clients")
async def create_client(client: Client):
    query = clients.insert().values(
        First_Name=client.First_Name,
        Last_Name=client.Last_Name,
        Username=client.Username,
        Password=client.Password,  # Store password as plain text (not recommended in production)
        Email=client.Email,
        BrokerID=client.BrokerID,
        isBroker=client.isBroker,
        isClient=client.isClient,
        isSysAdmin=client.isSysAdmin
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "Client created",
        "Id": result.lastrowid
    }

# Read Client
@app.get("/clients/{client_id}")
async def read_client(client_id: int):
    try:
        result = connection.execute(clients.select().where(clients.c.Id == client_id))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    for row in result:
        return dict(row)

# Update Client
@app.put("/clients/{client_id}")
async def update_client(client_id: int, client: Client):
    query = clients.update().where(clients.c.Id == client_id).values(
        First_Name=client.First_Name,
        Last_Name=client.Last_Name,
        Username=client.Username,
        Password=client.Password,  # Update password as plain text (not recommended in production)
        Email=client.Email,
        BrokerID=client.BrokerID,
        isBroker=client.isBroker,
        isClient=client.isClient,
        isSysAdmin=client.isSysAdmin
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "Client updated"
    }

# Delete Client
@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    try:
        result = connection.execute(clients.delete().where(clients.c.Id == client_id))
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "Client deleted"
    }