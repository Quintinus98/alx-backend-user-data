#!/usr/bin/env python3
"""Authentication"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Takes a password string argument and returns bytes.

    Returns: The returned bytes is a salted hash of the input password
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize Auth with DB"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Returns a User object"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a login is valid"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        password_bytes = password.encode("utf-8")
        res = bcrypt.checkpw(password_bytes, user.hashed_password)
        return res

    @property
    def _generate_uuid(self) -> str:
        """Generates a random uuid"""
        return uuid.uuid4()
