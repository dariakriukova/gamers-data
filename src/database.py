"""
Database schema for user data loaded from "Wild Wild Chords" and "HarmonicaBots" games.
"""

from sqlalchemy import ForeignKey, Date, UniqueConstraint
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
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    gender: Mapped[str]
    dob: Mapped[date] = mapped_column(Date)
    registration_date: Mapped[date] = mapped_column(Date)
    nationality: Mapped[str]
    region_id: Mapped[int] = mapped_column(ForeignKey('regions.id'))
    region: Mapped["Region"] = relationship("Region", back_populates="users")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Region(Base):
    __tablename__ = 'regions'
    __table_args__ = (UniqueConstraint("city", "state"),)
    
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[list["User"]] = relationship("User", back_populates="region")
    
engine = create_engine("sqlite:///wwc_hb.db", echo=True)
Base.metadata.create_all(engine)
