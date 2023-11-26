# Libraries
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
# import os

# Internal Imports
from crud_routing import create_table_routes
from model.broker import brokers_table, BrokerModel
from model.client import clients, Client
from model.property import properties, Property
from model.offer import offers, Offer
from model.favourite import favourites, Favourite

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
    # Load the URL from the secret variable
    # load_dotenv()
    # db_url = os.getenv("URL")
    db_url = "mysql://concordiadataba:password123@db4free.net:3306/soen341"
    
    engine = create_engine(db_url, echo = True)
    connection = engine.connect()

except Exception as e:
    print(f"Could not connect to database: {e}")

# Creating the Routes
create_table_routes(brokers_table, BrokerModel, connection, app)
create_table_routes(clients, Client, connection, app)
create_table_routes(properties, Property, connection, app)
create_table_routes(offers, Offer, connection, app)
create_table_routes(favourites, Favourite, connection, app)