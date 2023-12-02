#!/usr/bin/python3
""" holds class Courses"""

from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Table
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint as Check
from sqlalchemy.orm import relationship

from models.instructor import Instructor


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
    approved = Column(Boolean(), nullable=False, default=False)
    hours = Column(Integer, nullable=False)
    num_sections = Column(Integer, nullable=False, default=0)
    num_enrolled = Column(Integer, nullable=False, default=0)

    sections = relationship("Section", backref="course", cascade='all, delete-orphan')

    category_id = Column(String(60),
                         ForeignKey('categories.id'),
                         nullable=True)
    instructor_id = Column(String(60),
                           ForeignKey('instructors.id'),
                           nullable=False)
    students = relationship('Student',
                            secondary='enrollments', viewonly=False,
                            backref='courses')

    def to_dict(self):
        """returns dict representation of course"""
        from models import storage
        new_dict = super().to_dict()
        instructor = storage.get(Instructor, self.instructor_id)
        if instructor:
            new_dict['instructor_name'] = instructor.user.name
        # new_dict['total_students'] = instructor.total_students
        new_dict['sections'] = [section.to_dict() for section in self.sections]
        # new_dict['students'] = [student.to_dict() for student in self.students]
        return new_dict
