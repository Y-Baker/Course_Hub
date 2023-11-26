#!/usr/bin/python3

from models.base_model import BaseModel, Base
from models.base_model_role import BaseRole
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Admin(BaseRole, Base):
    """Reapresntation for Admin"""
    __tablename__ = 'admins'
    user = relationship("User", backref="admin")
    id = Column(String(60), ForeignKey('users.id'), primary_key=True)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
