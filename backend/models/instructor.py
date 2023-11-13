#!/usr/bin/python3

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from models.user import User

class Instructor(User):
    """Reapresntation for Instructor"""
    __tablename__ = 'students'
    total_students =  Column(Integer, nullable=False)
    courses = relationship('Course', backref='instructor')

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
