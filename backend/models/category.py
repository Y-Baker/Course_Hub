#!/usr/bin/python3
""" holds class Category"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models

class Category(BaseModel, Base):
    """Reapresntation of Category class"""
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False)
    courses = relationship('Course', backref='Category')
    students = relationship('models.student.Student', backref='Category')
    student_id = Column(String(60), ForeignKey('students.id'))

    def __init__(self, *args, **kwargs):
        """initializes Category"""
        super().__init__(*args, **kwargs)
