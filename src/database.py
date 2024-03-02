"""
Database schema for user data loaded from "Wild Wild Chords" and "HarmonicaBots" games.
"""

from sqlalchemy import ForeignKey, Date, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import date


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    gender: Mapped[str]
    dob: Mapped[date] = mapped_column(Date)
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


engine = create_engine("sqlite:///wwc_hb.db", echo=True)
Base.metadata.create_all(engine)


def upsert_region(session, region_data):
    region = session.query(Region).filter_by(**region_data).first()
    if not region:
        region = Region(**region_data)
        session.add(region)
        try:
            session.flush()
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError {e}")
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
        print(f"SQLAlchemyError occurred: {e}")
