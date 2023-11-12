#!/usr/bin/python3
""" holds class Lesson"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Lesson(BaseModel, Base):
    """Representation of a Lesson """
    __tablename__ = 'lessons'
    name = Column(String(128), nullable=False)
    lesson_num = Column(Integer, nullable=False, autoincrement=True)
    completed = Column(Boolean, nullable=False, default=False)

    section_id = Column(String(60),
                        ForeignKey('sections.id'),
                        nullable=False)
