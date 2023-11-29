#!/usr/bin/python3
"""service for instructor"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.instructor import Instructor


class InstructorService:
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
        
    def get_instructors(self, page, per_page):
        """method to paginate instructors"""
        offset = (page - 1) * per_page

        results = self.__session.query(Instructor)\
            .offset(offset)\
                .limit(per_page).all()
        return results
