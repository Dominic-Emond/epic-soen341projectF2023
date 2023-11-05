from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.schemas import PropertyCreate, PropertyUpdate, Property as PropertySchema
from models.property import Property
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/properties/", response_model=PropertySchema)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    new_property = Property(**property.dict())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property

@router.put("/properties/{property_id}", response_model=PropertySchema)
def update_property(property_id: int, property_update: PropertyUpdate, db: Session = Depends(get_db)):
    existing_property = db.query(Property).filter_by(Id=property_id).first()
    if existing_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    for field, value in property_update.dict().items():
        if value is not None:
            setattr(existing_property, field, value)

    db.commit()
    return existing_property

@router.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    existing_property = db.query(Property).filter_by(Id=property_id).first()
    if existing_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    db.delete(existing_property)
    db.commit()
    return {"message": "Property deleted"}

@router.get("/properties/{property_id}", response_model=PropertySchema)
def read_property(property_id: int, db: Session = Depends(get_db)):
    _property = db.query(Property).filter_by(Id=property_id).first()
    if _property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return _property
