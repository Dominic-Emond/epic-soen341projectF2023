from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, LargeBinary
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Could not connect to database: {e}")

meta = MetaData()

# Image Table
Base = declarative_base()

class ImageDB(Base):
    __tablename__ = 'Image'
    Id = Column(Integer, primary_key=True, index=True)
    Filename = Column(String, index=True)
    Description = Column(String)
    PropertyID = Column(Integer, ForeignKey('Property.Id'))
    ImageData = Column(LargeBinary)

# Create the table
Base.metadata.create_all(bind=engine)

# Image Class (Pydantic model)
class Image(BaseModel):
    Filename: str
    Description: str
    PropertyID: int
    ImageData: bytes

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations

# Create Image
@app.post("/images")
async def create_image(image: Image, db: Session = Depends(get_db)):
    db_image = ImageDB(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return {
        "message": "Image created",
        "Id": db_image.Id
    }

# Read Image
@app.get("/images/{image_id}")
async def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(ImageDB).filter(ImageDB.Id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return {
        "Id": db_image.Id,
        "Filename": db_image.Filename,
        "Description": db_image.Description,
        "PropertyID": db_image.PropertyID
        # Additional fields as needed
    }

# Upload Image
@app.post("/uploadimage/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read the contents of the file
    contents = await file.read()

    # Save the image data to the database
    db_image = ImageDB(Filename=file.filename, ImageData=contents)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return {"filename": file.filename, "id": db_image.Id}

# Search Images by PropertyID
@app.get("/searchimages/{property_id}")
async def search_images(property_id: int, db: Session = Depends(get_db)):
    db_images = db.query(ImageDB).filter(ImageDB.PropertyID == property_id).all()
    return [
        {
            "Id": db_image.Id,
            "Filename": db_image.Filename,
            "Description": db_image.Description,
            "PropertyID": db_image.PropertyID
            # Additional fields as needed
        }
        for db_image in db_images
    ]
