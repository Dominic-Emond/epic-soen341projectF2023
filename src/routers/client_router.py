from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.schemas import ClientCreate, ClientUpdate, Client as ClientSchema
from models.client import Client
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/clients/", response_model=ClientSchema)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.put("/clients/{client_id}", response_model=ClientSchema)
def update_client(client_id: int, client_update: ClientUpdate, db: Session = Depends(get_db)):
    existing_client = db.query(Client).filter_by(Id=client_id).first()
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    for field, value in client_update.dict().items():
        if value is not None:
            setattr(existing_client, field, value)

    db.commit()
    return existing_client

@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    existing_client = db.query(Client).filter_by(Id=client_id).first()
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(existing_client)
    db.commit()
    return {"message": "Client deleted"}

@router.get("/clients/{client_id}", response_model=ClientSchema)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter_by(Id=client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
