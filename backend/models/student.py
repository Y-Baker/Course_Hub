#!/usr/bin/python3

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.category import Category
from models.base_model import BaseModel, Base
from models.base_model_role import BaseRole
from models.user import User


class Student(BaseRole, Base):
    """Reapresntation for Student"""
    __tablename__ = 'students'
    interested = Column(String(60), ForeignKey('categories.id'),
                        nullable=True)
    # categories = relationship('Category', backref='student')
    user = relationship("User", backref="student")
    id = Column(String(60), ForeignKey('users.id'), primary_key=True)
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
