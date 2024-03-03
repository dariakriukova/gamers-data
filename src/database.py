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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=True)
    dob: Mapped[date] = mapped_column(Date, nullable=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=True)
    nationality: Mapped[str] = mapped_column(nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    region: Mapped["Region"] = relationship("Region", back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (UniqueConstraint("city", "state"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(nullable=True)
    users: Mapped[list["User"]] = relationship("User", back_populates="region")


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


def upsert_user(session, user_data, region):
    try:
        user = session.query(User).filter_by(email=user_data["email"]).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.region = region
        else:
            user = User(**user_data, region=region)
            session.add(user)
        session.flush()
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"SQLAlchemyError occurred: {e}")


def setup_db(db_name):
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
