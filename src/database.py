"""
Database schema for user data loaded from "Wild Wild Chords" and "HarmonicaBots" games.
"""

from sqlalchemy import ForeignKey, Date, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import date
import logging
import os


# A base class for all model classes that represent database tables
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    # email is always unique and required when registering
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=True)
    dob: Mapped[date] = mapped_column(Date, nullable=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=True)
    nationality: Mapped[str] = mapped_column(nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    region: Mapped["Region"] = relationship("Region", back_populates="users")
    wwc: Mapped[bool] = mapped_column(default=False)
    hb: Mapped[bool] = mapped_column(default=False)

    # user's id and email to string for debugging
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Region(Base):
    __tablename__ = "regions"
    # city may not be unique, but suponsingly city+state pair is
    __table_args__ = (UniqueConstraint("city", "state"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(nullable=True)
    users: Mapped[list["User"]] = relationship("User", back_populates="region")


# update an existing region or insert new
def upsert_region(session, region_data):
    region = session.query(Region).filter_by(**region_data).first()
    if not region:
        region = Region(**region_data)
        session.add(region)
        try:
            session.flush()
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError occurred: {e}")
            session.rollback()
    return region


def upsert_user(session, user_data):
    try:
        # the first matching record is sufficient to determine existence
        user = session.query(User).filter_by(email=user_data["email"]).first()
        if user:
            for key, value in user_data.items():
                # updating the user's attributes dynamically based on user_data
                setattr(user, key, value)
        else:
            user = User(**user_data)
            session.add(user)
        session.flush()
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"SQLAlchemyError occurred: {e}")


def get_engine(db_name):
    engine = create_engine(f"sqlite:///{db_name}")

    if not os.path.exists(db_name):
        try:
            Base.metadata.create_all(engine)
            logging.info(f"Database and tables are created: {db_name}")
        except OperationalError as e:
            logging.error(f"An error occurred during table creation: {e}")
    else:
        logging.info(f"Database already exists, connecting to: {db_name}")

    return engine
