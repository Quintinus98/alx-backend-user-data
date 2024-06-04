#!/usr/bin/env python3
"""Auth Class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Does the path require authentication? True/False"""
        if path is None:
            return True
        if not excluded_paths:
            return True
        normalized_path = path if path.endswith("/") else path + "/"
        if normalized_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the Authorization headers or None"""
        if request is None:
            return None

        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user"""
        return None
