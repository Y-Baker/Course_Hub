#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Admin(BaseModel, Base):
    """Reapresntation for Admin"""
    __tablename__ = 'admins'
    id = Column(String(60), ForeignKey('users.id'), primary_key=True)

    # user = relationship("User", backref="admin")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
