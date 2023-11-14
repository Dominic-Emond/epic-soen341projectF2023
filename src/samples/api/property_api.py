from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Boolean, Float
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

# Property Table
properties = Table(
    'Property', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('Address', String, nullable=False),
    Column('City', String, nullable=False),
    Column('Price', Float, nullable=False),
    Column('Bedrooms', Integer, nullable=False),
    Column('Bathrooms', Integer, nullable=False),
    Column('Size_SqFt', Float, nullable=False),
    Column('IsAvailable', Boolean, default=True),
    Column('BrokerID', Integer),
)

# Property Class (Pydantic model)
class Property(BaseModel):
    Address: str
    City: str
    Price: float
    Bedrooms: int
    Bathrooms: int
    Size_SqFt: float
    IsAvailable: bool = True
    BrokerID: int = None

# CRUD Operations

# Create Property
@app.post("/properties")
async def create_property(property: Property):
    query = properties.insert().values(
        Address=property.Address,
        City=property.City,
        Price=property.Price,
        Bedrooms=property.Bedrooms,
        Bathrooms=property.Bathrooms,
        Size_SqFt=property.Size_SqFt,
        IsAvailable=property.IsAvailable,
        BrokerID=property.BrokerID
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "Property created",
        "Id": result.lastrowid
    }

# Read Property
@app.get("/properties/{property_id}")
async def read_property(property_id: int):
    try:
        result = connection.execute(properties.select().where(properties.c.Id == property_id))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    for row in result:
        return dict(row)

# Update Property
@app.put("/properties/{property_id}")
async def update_property(property_id: int, property: Property):
    query = properties.update().where(properties.c.Id == property_id).values(
        Address=property.Address,
        City=property.City,
        Price=property.Price,
        Bedrooms=property.Bedrooms,
        Bathrooms=property.Bathrooms,
        Size_SqFt=property.Size_SqFt,
        IsAvailable=property.IsAvailable,
        BrokerID=property.BrokerID
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "Property updated"
    }

# Delete Property
@app.delete("/properties/{property_id}")
async def delete_property(property_id: int):
    try:
        result = connection.execute(properties.delete().where(properties.c.Id == property_id))
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "Property deleted"
    }

# Search Properties by City
@app.get("/searchproperties/{city}")
async def search_properties(city: str):
    try:
        result = connection.execute(properties.select().where(properties.c.City.like(f"%{city}%")))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    rows = [dict(row) for row in result]

    return rows
