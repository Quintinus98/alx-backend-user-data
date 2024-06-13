#!/usr/bin/env python3
"""Authentication"""
import bcrypt
from db import DB
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Takes a password string argument and returns bytes.

    Returns: The returned bytes is a salted hash of the input password
    """
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize Auth with DB"""
        self._db = DB()

    def register_user(self, email, password):
        """Returns a User object"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)

            return new_user
        else:
            raise ValueError(f"User {email} already exists")
