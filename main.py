from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import model
from model import UserComplain                         
from sqlalchemy.orm import Session
from database import engine, sessionlocal
from typing import Annotated, Optional
from pydantic import BaseModel                        
from fastapi.responses import JSONResponse
from Authentication.auth import token_decode
from Authentication import auth
from Admin import admin


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(admin.drive)


def open_database():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(open_database)]
user_dependency = Annotated[dict, Depends(token_decode)]


@app.get('/Showallcomplain')
def ShowAllComplain(db: db_dependency):
    return db.query(UserComplain).all()


# -------------------------- Complain Create -------------------------- #
class ComplainModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    image: Optional[str] = None


@app.post('/complain_create')
def Complain_Create(db: db_dependency, user: user_dependency, complain: ComplainModel):

    new_complain = UserComplain(                      
        title=complain.title,
        description=complain.description,
        category=complain.category,
        location=complain.location,
        image=complain.image,
        user_id=user.get('id')
    )

    db.add(new_complain)
    db.commit()
    db.refresh(new_complain)

    return JSONResponse(status_code=201, content={"message": "Complain Created Successfully"})


# -------------------------- Complain List -------------------------- #
@app.get('/ComplainList')
def Show_Complain_List(db: db_dependency, user: user_dependency):

    return db.query(UserComplain).filter(UserComplain.user_id == user.get('id')).all()
