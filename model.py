from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


class UserComplain(Base):
    __tablename__ = 'usercomplain'

    complain_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    category = Column(String)
    location = Column(String)
    image = Column(String, nullable=True)
    status = Column(String, default='Pending')
    create_at = Column(DateTime, default=datetime.now)
    user = relationship("Users")