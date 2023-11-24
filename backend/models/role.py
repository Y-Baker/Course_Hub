#!/usr/bin/python3
""" holds class Role"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Role(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'roles'
    name = Column(String(45), nullable=False, unique=True)
    

    def __init__(self, *args, **kwargs):
        """initializes role"""
        super().__init__(*args, **kwargs)
