from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.schemas import BrokerCreate, BrokerUpdate, Broker as BrokerSchema
from models.broker import Broker
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/brokers/", response_model=BrokerSchema)
def create_broker(broker: BrokerCreate, db: Session = Depends(get_db)):
    new_broker = Broker(**broker.dict())
    db.add(new_broker)
    db.commit()
    db.refresh(new_broker)
    return new_broker

@router.put("/brokers/{broker_id}", response_model=BrokerSchema)
def update_broker(broker_id: int, broker_update: BrokerUpdate, db: Session = Depends(get_db)):
    existing_broker = db.query(Broker).filter_by(Id=broker_id).first()
    if existing_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")

    for field, value in broker_update.dict().items():
        if value is not None:
            setattr(existing_broker, field, value)

    db.commit()
    return existing_broker

@router.delete("/brokers/{broker_id}")
def delete_broker(broker_id: int, db: Session = Depends(get_db)):
    existing_broker = db.query(Broker).filter_by(Id=broker_id).first()
    if existing_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")

    db.delete(existing_broker)
    db.commit()
    return {"message": "Broker deleted"}

@router.get("/brokers/{broker_id}", response_model=BrokerSchema)
def read_broker(broker_id: int, db: Session = Depends(get_db)):
    print("Goes Here!")
    broker = db.query(Broker).filter_by(Id=broker_id).first()
    print("Goes Here!")
    if broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return broker
