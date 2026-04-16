from fastapi import Depends
from sqlmodel import Session
from .database import get_session

def get_db_session(session: Session = Depends(get_session)):
    return session