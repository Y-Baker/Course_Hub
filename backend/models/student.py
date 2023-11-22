#!/usr/bin/python3

from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.category import Category
from models.base_model import BaseModel, Base


class Student(BaseModel, Base):
    """Reapresntation for Student"""
    __tablename__ = 'students'
    id = Column(String(60), ForeignKey('users.id'), primary_key=True)

    interested = Column(String(60), ForeignKey('categories.id'), nullable=False)
    categories = relationship('Category', backref='Student')
    # user = relationship("User", backref="student")
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
