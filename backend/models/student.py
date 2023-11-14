#!/usr/bin/python3

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.category import Category
from models.base_model import BaseModel, Base
from models.user import User


class Student(BaseModel, Base):
    """Reapresntation for Student"""
    __tablename__ = 'students'
    interested = Column(Integer, nullable=False)
    categories = relationship('Category', backref='student')
    user = relationship("User", backref="student")
    user_id = Column(String(60), ForeignKey('users.id'), unique=True)
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
