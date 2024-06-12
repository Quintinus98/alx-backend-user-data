#!/usr/bin/env python3
""" SQLAlchemy class """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Column
from typing import Optional


Base = declarative_base()


class User(Base):
    """Class User"""

    __tablename__ = "users"

    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # email: Mapped[str] = mapped_column(String(250))
    # hashed_password: Mapped[str] = mapped_column(String(250))
    # session_id: Mapped[Optional[str]] = mapped_column(String(250))
    # reset_token: Mapped[Optional[str]] = mapped_column(String(250))
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
