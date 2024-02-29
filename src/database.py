from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    gender = Column(String)
    dob = Column(Date)
    registration_date = Column(Date)
    country_or_region = Column(String)
    picture_url = Column(String)
    nationality = Column(String)

engine = create_engine('sqlite:///wwc_hb.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()