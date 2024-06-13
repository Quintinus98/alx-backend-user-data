#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from typing import Any
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves a user to the database

        Required: Accepts two arguments
        -   email
        -   hashed_password

        Return: A user object
        """
        user_obj = User(email=email, hashed_password=hashed_password)
        self._session.add(user_obj)
        self._session.commit()
        return user_obj

    def find_user_by(self, **kwargs: Any) -> User:
        """This method takes in arbitrary keyword arguments and
        filters the method's input arguments.

        Return: The first row found in the users table
        """
        if not kwargs:
            raise InvalidRequestError
        allowed_keys = User.__table__.columns.keys()  # User table Keys
        for key in kwargs.keys():
            if key not in allowed_keys:
                raise InvalidRequestError
        my_user = self._session.query(User).filter_by(**kwargs).first()
        if not my_user:
            raise NoResultFound
        return my_user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """Takes a user_id and arbitrary keyword arguments

        Return: None
        """
        user_obj = self.find_user_by(id=user_id)
        valid_attr = User.__table__.columns.keys()

        # check key in kwargs are valid
        for key in kwargs.keys():
            if key not in valid_attr:
                raise ValueError
        # Update the user object.
        for key, val in kwargs.items():
            setattr(user_obj, key, val)

        # commit changes to the db
        self._session.commit()
