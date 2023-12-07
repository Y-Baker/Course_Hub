#!/usr/bin/python3
"""service for instructor"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base


class SessionManagement:
    __engine = None
    session = None

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
        # sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # Session = scoped_session(sess_factory)
        # self.__session = Session


    def reload(self):
        """reloads data from the database"""
        print("calling reload")
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.session = scoped_session(sess_factory)

    def close(self):
        """call remove() method on the private session attribute"""
        print("calling close")
        self.session.remove()
