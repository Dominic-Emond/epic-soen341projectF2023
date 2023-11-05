from pydantic import BaseModel
from typing import Optional

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
