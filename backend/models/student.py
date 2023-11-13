#!/usr/bin/python3

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from models.user import User

class Student(User):
    """Reapresntation for Student"""
    interested = Column(Integer, nullable=False)
    categories = relationship('Category', backref='Student')

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
