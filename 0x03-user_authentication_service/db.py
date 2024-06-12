#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db")
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

    def add_user(self, email, hashed_password):
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

    def find_user_by(self, **kwargs):
        """This method takes in arbitrary keyword arguments and
        filters the method's input arguments.

        Return: The first row found in the users table
        """
        if not kwargs:
            raise InvalidRequestError("No query arguments were passed")
        allowed_keys = [
            "email",
            "hashed_password",
            "session_id",
            "reset_token",
        ]
        for key in kwargs.keys():
            if key not in allowed_keys:
                raise InvalidRequestError("Wrong query arguments were passed")
        my_user = self._session.query(User).filter_by(**kwargs).first()
        if not my_user:
            raise NoResultFound("No results were found")
        return my_user

    def update_user(self, user_id, **kwargs):
        """Takes a user_id and arbitrary keyword arguments

        Return: None
        """
        if not user_id or not isinstance(user_id, int):
            raise ValueError
        user_obj = self.find_user_by(id=user_id)
