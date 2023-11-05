from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.schemas import UserCreate, UserUpdate, User as UserSchema  # Rename User to UserSchema
from models.user import User
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{username}", response_model=UserSchema)
def update_user(username: str, user_update: UserUpdate, db: Session = Depends(get_db)):  # Rename user to user_update
    existing_user = db.query(User).filter_by(Username=username).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.dict().items():  # Rename user to user_update
        if value is not None:
            setattr(existing_user, field, value)

    db.commit()
    return existing_user

@router.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter_by(Username=username).first()  # Rename user to user_to_delete
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_to_delete)  # Rename user to user_to_delete
    db.commit()
    return {"message": "User deleted"}

@router.get("/users/{username}", response_model=UserSchema)
def read_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(Username=username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
