#!/usr/bin/python3
""" holds class Courses"""

from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Table
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint as Check
from sqlalchemy.orm import relationship

# association table between Courses and Students
enrollments = Table('enrollments', Base.metadata,
                    Column('student_id', String(60),
                           ForeignKey('students.id'),
                           primary_key=True, nullable=False),
                    Column('course_id', String(60),
                           ForeignKey('courses.id'),
                           primary_key=True, nullable=False),
                    Column('completed', Integer,
                           Check('completed >= 0 AND completed <= 100'),
                           nullable=False),
                    Column('enrolled_date', DateTime, default=datetime.utcnow)
                    )


class Course(BaseModel, Base):
    """Representation of a Course """
    __tablename__ = 'courses'
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    hours = Column(Integer, nullable=False)
    num_sections = Column(Integer, nullable=False, default=0)
    num_enrolled = Column(Integer, nullable=False, default=0)

    sections = relationship("Section", backref="course")

    category_id = Column(String(60),
                         ForeignKey('categories.id'),
                         nullable=True)
    instructor_id = Column(String(60),
                           ForeignKey('instructors.id'),
                           nullable=False)

    students = relationship('Student',
                            secondary='enrollments', viewonly=False,
                            backref='courses')
