# Import necessary libraries
from fastapi import FastAPI, HTTPException
from mysqlx import XSession
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
# Create a FastAPI instance
app = FastAPI()

# Define SQLAlchemy models
Base = declarative_base()

# Create a SQLAlchemy engine and session
DATABASE_URL = "mysql://host/soen341"
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
    Image = Column(String)  

# Create the tables in the database
Base.metadata.create_all(bind=engine)


def create_user(username, password, email, broker_id, is_broker, is_client, is_sys_admin):
    new_user = User(Username=username, Password=password, Email=email, BrokerID=broker_id, isBroker=is_broker, isClient=is_client, isSysAdmin=is_sys_admin)
    XSession.add(new_user)
    SessionLocal.commit()

def read_user(username):
    return SessionLocal.query(User).filter_by(Username=username).first()

def update_user(username, password=None, email=None, broker_id=None, is_broker=None, is_client=None, is_sys_admin=None):
    user = SessionLocal.query(User).filter_by(Username=username).first()
    if password:
        user.Password = password
    if email:
        user.Email = email
    if broker_id:
        user.BrokerID = broker_id
    if is_broker is not None:
        user.isBroker = is_broker
    if is_client is not None:
        user.isClient = is_client
    if is_sys_admin is not None:
        user.isSysAdmin = is_sys_admin
    SessionLocal.commit()

def delete_user(username):
    user = SessionLocal.query(User).filter_by(Username=username).first()
    SessionLocal.delete(user)
    SessionLocal.commit()


def add_property(broker_id, address, price):
    new_property = Property(Broker_Id=broker_id, Address=address, Price=price)
    SessionLocal.add(new_property)
    SessionLocal.commit()
    SessionLocal.refresh(new_property)
    return new_property.Id

def update_property(property_id, broker_id=None, address=None, price=None):
    existing_property = SessionLocal.query(Property).filter_by(Id=property_id).first()
    if broker_id is not  None:
        existing_property.Broker_Id = broker_id
    if address is not None:
        existing_property.Address = address
    if price is not None:
        existing_property.Price = price
    SessionLocal.commit()

def delete_property(property_id):
    existing_property = SessionLocal.query(Property).filter_by(Id=property_id).first()
    SessionLocal.delete(existing_property)
    SessionLocal.commit()

def add_image(property_id, image):
    new_image = Image(Property_Id=property_id, Image=image)
    SessionLocal.add(new_image)
    SessionLocal.commit()
    SessionLocal.refresh(new_image)
    return new_image.Id

def update_image(image_id, property_id=None, image=None):
    new_image = SessionLocal.query(Image).filter_by(Id=image_id).first()
    if property_id is not None:
        new_image.Property_Id = property_id
    if new_image is not None:
        new_image.Image = image
    SessionLocal.commit()

def delete_image(image_id):
    image = SessionLocal.query(Image).filter_by(Id=image_id).first()
    SessionLocal.delete(image)
    SessionLocal.commit()

def get_property_images(property_id):
    return SessionLocal.query(Image).filter_by(Property_Id=property_id).all()

def get_properties_by_broker_id(broker_id):
    return SessionLocal.query(Property).filter_by(Broker_Id=broker_id).all()

def get_user_properties(username):
    user = read_user(username)
    if user:
        return SessionLocal.query(Property).filter_by(Broker_Id=user.BrokerID).all()
    else:
        return []

def get_user_images(username):
    user_properties = get_user_properties(username)
    user_images = []
    for property in user_properties:
        user_images.extend(get_property_images(property.Id))
    return user_images

def get_property_details(property_id):
    existing_property = SessionLocal.query(Property).filter_by(Id=property_id).first()
    images = get_property_images(property_id)
    return existing_property, images

def get_all_properties():
    return SessionLocal.query(Property).all()

def get_all_users():
    return SessionLocal.query(User).all()

def get_all_images():
    return SessionLocal.query(Image).all()

def get_property_by_id(property_id):
    return SessionLocal.query(Property).filter_by(Id=property_id).first()

def get_user_by_id(user_id):
    return SessionLocal.query(User).filter_by(Id=user_id).first()

def get_image_by_id(image_id):
    return SessionLocal.query(Image).filter_by(Id=image_id).first()

def search_properties(address, price_min, price_max):
    return SessionLocal.query(Property).filter(Property.Address.like(f"%{address}%"), Property.Price >= price_min, Property.Price <= price_max).all()

def search_users(username):
    return SessionLocal.query(User).filter(User.Username.like(f"%{username}%")).all()

def search_images(image):
    return SessionLocal.query(Image).filter(Image.Image.like(f"%{image}%")).all()

def search_property_images(property_id, image):
    return SessionLocal.query(Image).filter(Image.Property_Id == property_id, Image.Image.like(f"%{image}%")).all()

def search_user_properties(username, property_id):
    user = read_user(username)
    if user:
        return SessionLocal.query(Property).filter(Property.Broker_Id == user.BrokerID, Property.Id == property_id).all()
    else:
        return []

def search_user_images(username, image_id):
    user_images = get_user_images(username)
    return [image for image in user_images if image.Id == image_id]

def read_user(username):
    return SessionLocal.query(User).filter_by(Username=username).first()

def read_broker(broker_id):
    return SessionLocal.query(Broker).filter_by(Id=broker_id).first()

def get_user_id(username):
    user = read_user(username)
    if user:
        return user.Id
    else:
        return None

def get_broker_id(broker_id):
    broker = read_broker(broker_id)
    if broker:
        return broker.Id
    else:
        return None

def create_user(username, password, email, broker_id=None):
    new_user = User(Username=username, Password=password, Email=email, BrokerID=broker_id)
    SessionLocal.add(new_user)
    SessionLocal.commit()
    SessionLocal.refresh(new_user)
    return new_user.Id

def update_user(user_id, username=None, password=None, email=None, broker_id=None):
    user = SessionLocal.query(User).filter_by(Id=user_id).first()
    if username is not None:
        user.Username = username
    if password is not None:
        user.Password = password
    if email is not None:
        user.Email = email
    if broker_id is not None:
        user.BrokerID = broker_id
    SessionLocal.commit()
    
def add_broker(first_name, last_name, email_address, username, password):
    new_broker = Broker(First_Name=first_name, Last_Name=last_name, Email_Address=email_address, Username=username, Pass=password)
    SessionLocal.add(new_broker)
    SessionLocal.commit()
    SessionLocal.refresh(new_broker)
    return new_broker.Id

def update_broker(broker_id, first_name=None, last_name=None, email_address=None, username=None, password=None):
    existing_broker = SessionLocal.query(Broker).filter_by(Id=broker_id).first()
    if first_name:
        existing_broker.First_Name = first_name
    if last_name:
        existing_broker.Last_Name = last_name
    if email_address:
        existing_broker.Email_Address = email_address
    if username:
        existing_broker.Username = username
    if password:
        existing_broker.Pass = password
    SessionLocal.commit()

def delete_broker(broker_id):
    existing_broker = SessionLocal.query(Broker).filter_by(Id=broker_id).first()
    SessionLocal.delete(existing_broker)
    SessionLocal.commit()

def add_client(first_name, last_name, client_type, username, password):
    new_client = Client(First_Name=first_name, Last_Name=last_name, Type=client_type, Username=username, Pass=password)
    SessionLocal.add(new_client)
    SessionLocal.commit()
    SessionLocal.refresh(new_client)
    return new_client.Id

def update_client(client_id, first_name=None, last_name=None, client_type=None, username=None, password=None):
    existing_client = SessionLocal.query(Client).filter_by(Id=client_id).first()
    if first_name:
        existing_client.First_Name = first_name
    if last_name:
        existing_client.Last_Name = last_name
    if client_type:
        existing_client.Type = client_type
    if username:
        existing_client.Username = username
    if password:
        existing_client.Pass = password
    SessionLocal.commit()

def read_client(client_id):
    return SessionLocal.query(Client).filter_by(Id=client_id).first()

def delete_client(client_id):
    existing_client = SessionLocal.query(Client).filter_by(Id=client_id).first()
    SessionLocal.delete(existing_client)
    SessionLocal.commit()

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

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    Property_Id: Optional[int] = None
    Image: Optional[str] = None

class Image(ImageBase):
    Id: int


# Routes for FastAPI application (e.g., CRUD operations for User, Broker, etc.)


# Create a new user
@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    return create_user(**user.dict())

# Read user by username
@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    user = read_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# Update user by username
@app.put("/users/{username}", response_model=User)
def update_user(username: str, user: UserUpdate):
    updated_user = update_user(username, **user.dict())
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
# Delete user by username
@app.delete("/users/{username}")
def delete_user(username: str):
    deleted_user = delete_user(username)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

# Create a new property
@app.post("/properties/", response_model=Property)
def create_property(property: PropertyCreate):
    return add_property(**property.dict())

# Update property by property_id
@app.put("/properties/{property_id}", response_model=Property)
def update_property(property_id: int, property: PropertyUpdate):
    updated_property = update_property(property_id, **property.dict())
    if updated_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated_property

# Delete property by property_id
@app.delete("/properties/{property_id}")
def delete_property(property_id: int):
    deleted_property = delete_property(property_id)
    if deleted_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"message": "Property deleted"}

# Create a new broker
@app.post("/brokers/", response_model=Broker)
def create_broker(broker: BrokerCreate):
    return add_broker(**broker.dict())

# Read broker by broker_id
@app.get("/brokers/{broker_id}", response_model=Broker)
def read_broker(broker_id: int):
    broker = read_broker(broker_id)
    if broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return broker

# Update broker by broker_id
@app.put("/brokers/{broker_id}", response_model=Broker)
def update_broker(broker_id: int, broker: BrokerUpdate):
    updated_broker = update_broker(broker_id, **broker.dict())
    if updated_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return updated_broker

# Delete broker by broker_id
@app.delete("/brokers/{broker_id}")
def delete_broker(broker_id: int):
    deleted_broker = delete_broker(broker_id)
    if deleted_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return {"message": "Broker deleted"}

# Create a new client
@app.post("/clients/", response_model=Client)
def create_client(client: ClientCreate):
    return add_client(**client.dict())

# Read client by client_id
@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int):
    client = read_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Update client by client_id
@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: int, client: ClientUpdate):
    updated_client = update_client(client_id, **client.dict())
    if updated_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client

# Delete client by client_id
@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    deleted_client = delete_client(client_id)
    if deleted_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted"}

# Create a new image
@app.post("/images/", response_model=Image)
def create_image(image: ImageCreate):
    return add_image(**image.dict())

# Update image by image_id
@app.put("/images/{image_id}", response_model=Image)
def update_image(image_id: int, image: ImageUpdate):
    updated_image = update_image(image_id, **image.dict())
    if updated_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return updated_image

# Delete image by image_id
@app.delete("/images/{image_id}")
def delete_image(image_id: int):
    deleted_image = delete_image(image_id)
    if deleted_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
