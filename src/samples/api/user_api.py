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

# User Table
users = Table(
    'User', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True),
    Column('First_Name', String, nullable=False),
    Column('Last_Name', String, nullable=False),
    Column('Username', String, nullable=False),
    Column('Password', String, nullable=False),
    Column('Email', String, nullable=False),
    Column('BrokerID', Integer),
    Column('isBroker', Boolean, default=False),
    Column('isClient', Boolean, default=False),
    Column('isSysAdmin', Boolean, default=False)
)

# User Class (Pydantic model)
class User(BaseModel):
    First_Name: str
    Last_Name: str
    Username: str
    Password: str
    Email: str
    BrokerID: int = None
    isBroker: bool = False
    isClient: bool = False
    isSysAdmin: bool = False

# CRUD Operations

# Create User
@app.post("/users")
async def create_user(user: User):
    query = users.insert().values(
        First_Name=user.First_Name,
        Last_Name=user.Last_Name,
        Username=user.Username,
        Password=user.Password,  # Store password as plain text (not recommended in production)
        Email=user.Email,
        BrokerID=user.BrokerID,
        isBroker=user.isBroker,
        isClient=user.isClient,
        isSysAdmin=user.isSysAdmin
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "User created",
        "Id": result.lastrowid
    }

# Read Users

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    try:
        result = connection.execute(users.select().where(users.c.Id == user_id))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    for row in result:
        return dict(row)

# Update User
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    query = users.update().where(users.c.Id == user_id).values(
        First_Name=user.First_Name,
        Last_Name=user.Last_Name,
        Username=user.Username,
        Password=user.Password,  # Update password as plain text (not recommended in production)
        Email=user.Email,
        BrokerID=user.BrokerID,
        isBroker=user.isBroker,
        isClient=user.isClient,
        isSysAdmin=user.isSysAdmin
    )

    try:
        result = connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "User updated"
    }

# Delete User
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    try:
        result = connection.execute(users.delete().where(users.c.Id == user_id))
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    return {
        "message": "User deleted"
    }

# Search Users by Name
@app.get("/searchusers/{name}")
async def search_users(name: str):
    try:
        result = connection.execute(users.select().where(
            or_(
                users.c.First_Name.like(f"%{name}%"),
                users.c.Last_Name.like(f"%{name}%")
            )))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

    rows = [dict(row) for row in result]

    return rows