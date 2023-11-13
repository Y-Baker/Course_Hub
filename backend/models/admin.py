#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship

class Admin(BaseModel, Base):
    """Reapresntation for Admin"""
    __tablename__ = 'admins'
    user = relationship("User", backref="admin")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
