"""
Database schema for user data loaded from "Wild Wild Chords" and "HarmonicaBots" games.
"""

from sqlalchemy import ForeignKey, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import date

class Base(DeclarativeBase):
    pass
    

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    gender: Mapped[str]
    dob: Mapped[date] = mapped_column(Date)
    registration_date: Mapped[date] = mapped_column(Date)
    picture_url: Mapped[str]
    nationality: Mapped[str]
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    region: Mapped["Region"] = relationship(back_populates="children")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Region(Base):
    __tablename__ = 'region'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship("User", back_populates="region")
    
engine = create_engine("sqlite:///wwc_hb.db", echo=True)
Base.metadata.create_all(engine)
