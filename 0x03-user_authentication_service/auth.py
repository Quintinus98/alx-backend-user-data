#!/usr/bin/env python3
"""Authentication"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Takes a password string argument and returns bytes.

    Returns: The returned bytes is a salted hash of the input password
    """
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return hashed_password
