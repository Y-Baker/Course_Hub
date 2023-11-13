#!/usr/bin/python3

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Instructor(BaseModel, Base):
    """Reapresntation for Instructor"""
    __tablename__ = 'instructors'
    total_students =  Column(Integer, nullable=False)
    user = relationship("User", backref="instructor")
    # user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    courses = relationship('Course', backref='instructor')
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
