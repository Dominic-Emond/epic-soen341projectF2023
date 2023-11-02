# Import necessary libraries
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from sqlalchemy import LargeBinary
import base64

# Create a FastAPI instance
app = FastAPI()

# Define SQLAlchemy models
Base = declarative_base()

# Create a SQLAlchemy engine and session
DATABASE_URL = "mysql://soen341"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the User model
class User(Base):
    __tablename__ = "User"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(255), nullable=False)
    Last_Name = Column(String(255), nullable=False)
    Username = Column(String(255), nullable=False, unique=True)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False)
    BrokerID = Column(Integer)
    isBroker = Column(Boolean, default=False)
    isClient = Column(Boolean, default=False)
    isSysAdmin = Column(Boolean, default=False)

# Define the Broker model
class Broker(Base):
    __tablename__ = "Broker"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(255))
    Last_Name = Column(String(255))
    Email_Address = Column(String(255))
    Username = Column(String(255), unique=True)
    Pass = Column(String(255))

# Define the Client model
class Client(Base):
    __tablename__ = "Client"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(255))
    Last_Name = Column(String(255))
    Type = Column(String(255))
    Username = Column(String(255), unique=True)
    Pass = Column(String(255))

# Define the Property model
class Property(Base):
    __tablename__ = "Property"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Broker_Id = Column(Integer, ForeignKey("Broker.Id"))
    Address = Column(String(255))
    Price = Column(Float)

# Define the Image model
class Image(Base):
    __tablename__ = "Image"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Property_Id = Column(Integer, ForeignKey("Property.Id"))
    Image = Column(LargeBinary)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# CRUD operations for User, Broker, Client, Property, and Image models (add functions as needed)

# Define Pydantic models for request and response
from pydantic import BaseModel

class UserBase(BaseModel):
    Username: str
    Password: str
    Email: str
    BrokerID: Optional[int] = None
    isBroker: bool = False
    isClient: bool = False
    isSysAdmin: bool = False

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    Password: Optional[str] = None
    Email: Optional[str] = None
    BrokerID: Optional[int] = None
    isBroker: Optional[bool] = None
    isClient: Optional[bool] = None
    isSysAdmin: Optional[bool] = None

class User(UserBase):
    Id: int

class BrokerBase(BaseModel):
    First_Name: str
    Last_Name: str
    Email_Address: str
    Username: str

class BrokerCreate(BrokerBase):
    Pass: str

class BrokerUpdate(BaseModel):
    Pass: Optional[str] = None

class Broker(BrokerBase):
    Id: int

class ClientBase(BaseModel):
    First_Name: str
    Last_Name: str
    Type: str
    Username: str

class ClientCreate(ClientBase):
    Pass: str

class ClientUpdate(BaseModel):
    Pass: Optional[str] = None

class Client(ClientBase):
    Id: int

class PropertyBase(BaseModel):
    Broker_Id: int
    Address: str
    Price: float

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    Broker_Id: Optional[int] = None
    Address: Optional[str] = None
    Price: Optional[float] = None

class Property(PropertyBase):
    Id: int

class ImageBase(BaseModel):
    Property_Id: int
    Image: str

class ImageCreate(BaseModel):
    Property_Id: int
    Image: str  # The image data should be sent as a base64-encoded string

class ImageUpdate(BaseModel):
    Property_Id: Optional[int] = None
    Image: Optional[str] = None

class Image(ImageBase):
    Id: int

# CRUD operations for User, Broker, Client, Property, and Image models (add functions as needed)

# Create a new user
@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    new_user = User(**user.dict())
    SessionLocal.add(new_user)
    SessionLocal.commit()
    SessionLocal.refresh(new_user)
    return new_user

# Read user by username
@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    user = SessionLocal.query(User).filter_by(Username=username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user by username
@app.put("/users/{username}", response_model=User)
def update_user(username: str, user: UserUpdate):
    user = SessionLocal.query(User).filter_by(Username=username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user.dict().items():
        if value is not None:
            setattr(user, field, value)

    SessionLocal.commit()
    return user

# Delete user by username
@app.delete("/users/{username}")
def delete_user(username: str):
    user = SessionLocal.query(User).filter_by(Username=username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    SessionLocal.delete(user)
    SessionLocal.commit()
    return {"message": "User deleted"}

# Create a new broker
@app.post("/brokers/", response_model=Broker)
def create_broker(broker: BrokerCreate):
    new_broker = Broker(**broker.dict())
    SessionLocal.add(new_broker)
    SessionLocal.commit()
    SessionLocal.refresh(new_broker)
    return new_broker

# Read broker by broker_id
@app.get("/brokers/{broker_id}", response_model=Broker)
def read_broker(broker_id: int):
    broker = SessionLocal.query(Broker).filter_by(Id=broker_id).first()
    if broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return broker

# Update broker by broker_id
@app.put("/brokers/{broker_id}", response_model=Broker)
def update_broker(broker_id: int, broker: BrokerUpdate):
    existing_broker = SessionLocal.query(Broker).filter_by(Id=broker_id).first()
    if existing_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")

    for field, value in broker.dict().items():
        if value is not None:
            setattr(existing_broker, field, value)

    SessionLocal.commit()
    return existing_broker

# Delete broker by broker_id
@app.delete("/brokers/{broker_id}")
def delete_broker(broker_id: int):
    existing_broker = SessionLocal.query(Broker).filter_by(Id=broker_id).first()
    if existing_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")

    SessionLocal.delete(existing_broker)
    SessionLocal.commit()
    return {"message": "Broker deleted"}

# CRUD operations for Client model

# Create a new client
@app.post("/clients/", response_model=Client)
def create_client(client: ClientCreate):
    new_client = Client(**client.dict())
    SessionLocal.add(new_client)
    SessionLocal.commit()
    SessionLocal.refresh(new_client)
    return new_client

# Read client by client_id
@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int):
    client = SessionLocal.query(Client).filter_by(Id=client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Update client by client_id
@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: int, client: ClientUpdate):
    existing_client = SessionLocal.query(Client).filter_by(Id=client_id).first()
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    for field, value in client.dict().items():
        if value is not None:
            setattr(existing_client, field, value)

    SessionLocal.commit()
    return existing_client

# Delete client by client_id
@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    existing_client = SessionLocal.query(Client).filter_by(Id=client_id).first()
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    SessionLocal.delete(existing_client)
    SessionLocal.commit()
    return {"message": "Client deleted"}

# Create a new property
@app.post("/properties/", response_model=Property)
def create_property(property: PropertyCreate):
    new_property = Property(**property.dict())
    SessionLocal.add(new_property)
    SessionLocal.commit()
    SessionLocal.refresh(new_property)
    return new_property

# Update property by property_id
@app.put("/properties/{property_id}", response_model=Property)
def update_property(property_id: int, property: PropertyUpdate):
    existing_property = SessionLocal.query(Property).filter_by(Id=property_id).first()
    if existing_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    for field, value in property.dict().items():
        if value is not None:
            setattr(existing_property, field, value)

    SessionLocal.commit()
    return existing_property

# Delete property by property_id
@app.delete("/properties/{property_id}")
def delete_property(property_id: int):
    existing_property = SessionLocal.query(Property).filter_by(Id=property_id).first()
    if existing_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    SessionLocal.delete(existing_property)
    SessionLocal.commit()
    return {"message": "Property deleted"}

# Create a new image
@app.post("/images/", response_model=Image)
def create_image(image: ImageCreate):
    image_data = base64.b64decode(image.Image)
    new_image = Image(Property_Id=image.Property_Id, Image=image_data)
    SessionLocal.add(new_image)
    SessionLocal.commit()
    SessionLocal.refresh(new_image)
    return new_image

# Update image by image_id
@app.put("/images/{image_id}", response_model=Image)
def update_image(image_id: int, image: ImageUpdate):
    existing_image = SessionLocal.query(Image).filter_by(Id=image_id).first()
    if existing_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    for field, value in image.dict().items():
        if value is not None:
            setattr(existing_image, field, value)

    SessionLocal.commit()
    return existing_image

# Delete image by image_id
@app.delete("/images/{image_id}")
def delete_image(image_id: int):
    existing_image = SessionLocal.query(Image).filter_by(Id=image_id).first()
    if existing_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    SessionLocal.delete(existing_image)
    SessionLocal.commit()
    return {"message": "Image deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
