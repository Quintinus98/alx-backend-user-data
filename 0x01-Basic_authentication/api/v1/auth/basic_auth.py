#!/usr/bin/env python3
"""Basic Auth Class
"""
from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication"""

    def __init__(self) -> None:
        """Inherits from Auth"""
        super().__init__()

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[-1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode a Base64 string.

        Args:
            base64_authorization_header (str): Base64 string to be decoded.

        Returns:
            str: Decoded string in UTF-8 format, or None if any error occurs.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_auth_header = base64.b64decode(
                base64_authorization_header
            ).decode("utf-8")
            return decoded_auth_header
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user_email, user_pwd = decoded_base64_authorization_header.split(
            ":", 1
        )
        return (user_email, user_pwd)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """Returns the user instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        database_search = User.search({"email": user_email})
        if not database_search:
            return None
        user = database_search[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar("User"):
        """Overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        extracted_header = self.extract_base64_authorization_header(
            auth_header
        )
        decoded_header = self.decode_base64_authorization_header(
            extracted_header
        )
        credentials = self.extract_user_credentials(decoded_header)
        user_object = self.user_object_from_credentials(
            credentials[0], credentials[1]
        )
        return user_object
