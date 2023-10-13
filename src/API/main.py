from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a FastAPI instance
app = FastAPI()

# Define SQLAlchemy models
Base = declarative_base()

class Broker(Base):
    __tablename__ = "brokers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    phone = Column(String)

# Create the database engine and session
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Pydantic models for request and response
class BrokerCreate(BaseModel):
    name: str
    address: str
    phone: str

class BrokerUpdate(BaseModel):
    name: str
    address: str
    phone: str

class BrokerResponse(BrokerCreate):
    id: int

# Routes
@app.post("/brokers/", response_model=BrokerResponse)
def create_broker(broker: BrokerCreate):
    db = SessionLocal()
    db_broker = Broker(**broker.dict())
    db.add(db_broker)
    db.commit()
    db.refresh(db_broker)
    db.close()
    return JSONResponse(content=db_broker.dict(), status_code=201)

@app.get("/brokers/{broker_id}", response_model=BrokerResponse)
def read_broker(broker_id: int):
    db = SessionLocal()
    db_broker = db.query(Broker).filter(Broker.id == broker_id).first()
    db.close()
    if db_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return JSONResponse(content=db_broker.dict())

@app.put("/brokers/{broker_id}", response_model=BrokerResponse)
def update_broker(broker_id: int, broker: BrokerUpdate):
    db = SessionLocal()
    db_broker = db.query(Broker).filter(Broker.id == broker_id).first()
    if db_broker is None:
        db.close()
        raise HTTPException(status_code=404, detail="Broker not found")
    for key, value in broker.dict().items():
        setattr(db_broker, key, value)
    db.commit()
    db.refresh(db_broker)
    db.close()
    return JSONResponse(content=db_broker.dict())

@app.delete("/brokers/{broker_id}", response_model=BrokerResponse)
def delete_broker(broker_id: int):
    db = SessionLocal()
    db_broker = db.query(Broker).filter(Broker.id == broker_id).first()
    if db_broker is None:
        db.close()
        raise HTTPException(status_code=404, detail="Broker not found")
    db.delete(db_broker)
    db.commit()
    db.close()
    return JSONResponse(content=db_broker.dict())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)