# Libraries
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
# import os

# Internal Imports
from crud_routing import create_table_routes
from search_routing import create_search_route
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

# Creating the CRUD Routes
create_table_routes(brokers_table, BrokerModel, connection, app)
create_table_routes(clients, Client, connection, app)
create_table_routes(properties, Property, connection, app)
create_table_routes(offers, Offer, connection, app)
create_table_routes(favourites, Favourite, connection, app)

# Creating the Search Routes
create_search_route(brokers_table, [brokers_table.c.First_Name, brokers_table.c.Last_Name], BrokerModel, connection, app)
create_search_route(clients, [clients.c.First_Name, clients.c.Last_Name], Client, connection, app)
create_search_route(properties, [properties.c.Address, properties.c.City], Property, connection, app)