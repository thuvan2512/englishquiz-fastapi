from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy

DATABASE_URL = "mysql+mysqlconnector://root:25122k@localhost:3306/englishdb"
engine = create_engine(DATABASE_URL)

def get_database_session()-> sqlalchemy.orm.session.Session:
    Session = sessionmaker(bind=engine)
    return Session()

def get_model_orm() -> sqlalchemy.orm.DeclarativeMeta:
    model_orm = declarative_base()
    return model_orm

