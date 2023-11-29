#!/usr/bin/python3
"""service for course"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.course import Course
from models.section import Section
from models.lesson import Lesson
from models.category import Category
from models.instructor import Instructor


class CourseService:
    __engine = None
    __session = None

    def __init__(self):
        CH_MYSQL_USER = getenv('CH_MYSQL_USER')
        CH_MYSQL_PWD = getenv('CH_MYSQL_PWD')
        CH_MYSQL_HOST = getenv('CH_MYSQL_HOST')
        CH_MYSQL_DB = getenv('CH_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                format(CH_MYSQL_USER,
                                        CH_MYSQL_PWD,
                                        CH_MYSQL_HOST,
                                        CH_MYSQL_DB))
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
        
    def get_courses(self, page, per_page):
        """method to paginate courses"""
        offset = (page - 1) * per_page

        results = self.__session.query(Course)\
            .offset(offset)\
                .limit(per_page).all()
        return results

    def get_courses_by_instructor(self, instructor_id, page, per_page):
        """method to paginate courses"""
        offset = (page - 1) * per_page

        results = self.__session.query(Course)\
            .filter(Course.instructor_id == instructor_id)\
            .offset(offset)\
                .limit(per_page).all()
        return results

    def get_courses_by_category(self, category_id, page, per_page):
        """method to paginate courses"""
        offset = (page - 1) * per_page

        results = self.__session.query(Course)\
            .filter(Course.category_id == category_id)\
            .offset(offset)\
                .limit(per_page).all()
        return results

    def get_categories(self, page, per_page):
        """method to paginate categories"""
        offset = (page - 1) * per_page

        results = self.__session.query(Category)\
            .offset(offset)\
                .limit(per_page).all()
        return results

    def get_sections_by_course(self, course_id, page, per_page):
        """method to paginate sections"""
        offset = (page - 1) * per_page

        results = self.__session.query(Section)\
            .filter(Section.course_id == course_id)\
            .offset(offset)\
                .limit(per_page).all()
        return results

    def get_lessons_by_section(self, section_id, page, per_page):
        """method to paginate lessons"""
        offset = (page - 1) * per_page

        results = self.__session.query(Lesson)\
            .filter(Lesson.section_id == section_id)\
            .offset(offset)\
                .limit(per_page).all()
        return results
