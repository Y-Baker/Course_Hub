#!/usr/bin/python3

from models.user import User

class Admin(User):
    """Reapresntation for Admin"""
    __tablename__ = 'admins'

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
