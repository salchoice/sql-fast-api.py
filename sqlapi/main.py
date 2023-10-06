from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schema
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schema.User)
def create_user(user:schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_users_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already exists')
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=schema.User)
def read_user(db: Session = Depends(get_db)):
    db_user = crud.get_users(db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.post('/users/{user_id}/items', response_model=schema.Item)
def create_item_for_user(user_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get('/items/', response_model=schema.Item)
def read_items(skip: int = 0, limit: int=100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
