from fastapi import Depends, HTTPException, APIRouter       
from model import UserComplain                              
from sqlalchemy.orm import Session
from database import sessionlocal                          
from typing import Annotated
from fastapi.responses import JSONResponse
from Authentication.auth import token_decode


drive = APIRouter()


def open_database():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(open_database)]
user_dependency = Annotated[dict, Depends(token_decode)]


# ---------------------- All Complaints ---------------------- #
@drive.get('/admin/allcomplain')
def complain_show(db: db_dependency, user: user_dependency):
    if user.get('role') != 'admin':                         
        raise HTTPException(status_code=403, detail='Admin access required')   

    return db.query(UserComplain).all()


# ---------------------- Search by ID ---------------------- #
@drive.get('/admin_search_complain/{complain_id}')
def search_complain(db: db_dependency, user: user_dependency, complain_id: int):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')

    complain = db.query(UserComplain).filter(UserComplain.complain_id == complain_id).first() 

    if complain is None:
        raise HTTPException(status_code=404, detail='Complain ID Not Found')
    return complain


# ---------------------- Filter by Category ---------------------- #
@drive.get('/admin_filter_category')                        
def filter_by_category(db: db_dependency, user: user_dependency, category: str):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')

    results = db.query(UserComplain).filter(UserComplain.category == category).all()

    if not results:
        raise HTTPException(status_code=404, detail='No Complaint Found')
    return results


# ---------------------- Status: In Progress ---------------------- #
@drive.put('/admin_status_progress/{complain_id}')
def update_status_progress(db: db_dependency, user: user_dependency, complain_id: int):   
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')

    complain = db.query(UserComplain).filter(UserComplain.complain_id == complain_id).first()

    if complain is None:
        raise HTTPException(status_code=404, detail='Complain ID Not Found')

    complain.status = 'In Progress'
    db.commit()

    return {"message": "Complain In Progress"}            


# ---------------------- Status: Completed ---------------------- #
@drive.put('/admin_status_complete/{complain_id}')
def update_status_complete(db: db_dependency, user: user_dependency, complain_id: int): 
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')

    complain = db.query(UserComplain).filter(UserComplain.complain_id == complain_id).first()

    if complain is None:
        raise HTTPException(status_code=404, detail='Complain ID Not Found')

    complain.status = 'Completed'
    db.commit()

    return {"message": "Issue Solved"}                     