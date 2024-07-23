#!/usr/bin/env python3
"""Session Auth Class
"""
from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth
import base64
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session Authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user id based on a session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)