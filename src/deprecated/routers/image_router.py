from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.schemas import ImageCreate, ImageUpdate, Image as ImageSchema
from models.image import Image
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/images/", response_model=ImageSchema)
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    new_image = Image(**image.dict())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

@router.put("/images/{image_id}", response_model=ImageSchema)
def update_image(image_id: int, image_update: ImageUpdate, db: Session = Depends(get_db)):
    existing_image = db.query(Image).filter_by(Id=image_id).first()
    if existing_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    for field, value in image_update.dict().items():
        if value is not None:
            setattr(existing_image, field, value)

    db.commit()
    return existing_image

@router.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    existing_image = db.query(Image).filter_by(Id=image_id).first()
    if existing_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    db.delete(existing_image)
    db.commit()
    return {"message": "Image deleted"}

@router.get("/images/{image_id}", response_model=ImageSchema)
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter_by(Id=image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image
