"""to init db"""

from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import scoped_session, sessionmaker

CH_MYSQL_USER = getenv('CH_MYSQL_USER')
CH_MYSQL_PWD = getenv('CH_MYSQL_PWD')
CH_MYSQL_HOST = getenv('CH_MYSQL_HOST')
CH_MYSQL_DB = getenv('CH_MYSQL_DB')
CH_ENV = getenv('CH_ENV')
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                format(CH_MYSQL_USER,
                                        CH_MYSQL_PWD,
                                        CH_MYSQL_HOST, 
                                        CH_MYSQL_DB))
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
