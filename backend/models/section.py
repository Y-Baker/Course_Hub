#!/usr/bin/python3
""" holds class Sections"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Section(BaseModel, Base):
    """Representation of a Section """
    __tablename__ = 'sections'
    name = Column(String(128), nullable=False)
    section_num = Column(Integer, nullable=False, autoincrement=True)
    completed = Column(Boolean, nullable=False, default=False)

    course_id = Column(String(60),
                       ForeignKey('courses.id'),
                       nullable=False)

    lessons = relationship("Lesson", backref="section", cascade='all, delete-orphan')

    def check_complete(self):
        """Update complete state"""
        total = len(self.lessons)
        done = 0
        for lesson in self.lessons:
            if lesson.completed:
                done += 1
        if total == done:
            self.completed = True

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        self.check_complete()
