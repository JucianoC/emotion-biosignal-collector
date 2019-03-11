import configparser

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONFIG = configparser.ConfigParser()
CONFIG.read('alembic.ini')

engine = create_engine(CONFIG.get('alembic', 'sqlalchemy.url'))
Base = declarative_base()
Session = sessionmaker(bind=engine)
