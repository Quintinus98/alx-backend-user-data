#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from user import User
import requests

AUTH = Auth()

BASE_URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """register a user"""
    data = {
        email: email,
        password: password
    }
    res = requests.post(f"{BASE_URL}/users", data=data)
    expected = {"email": f"{email}", "message": "user created"}
    assert res.json() == expected


def log_in_wrong_password(email: str, password: str) -> None:
    """log in wrong password"""
    is_login_valid = AUTH.valid_login(email, password)
    assert is_login_valid == False


def log_in(email: str, password: str) -> str:
    """log in"""
    is_login_valid = AUTH.valid_login(email, password)
    assert is_login_valid == True
    return AUTH.create_session(email)


def profile_unlogged() -> None:
    """profile unlogged"""
    profile = AUTH.get_user_from_session_id(None)
    assert profile == None


def profile_logged(session_id: str) -> None:
    """profile logged"""
    profile = AUTH.get_user_from_session_id(session_id)
    assert type(profile) == User


def log_out(session_id: str) -> None:
    """log out"""
    user = AUTH.get_user_from_session_id(session_id)
    AUTH.destroy_session(user.id)
    assert AUTH.get_user_from_session_id(session_id) == None


def reset_password_token(email: str) -> str:
    """reset password token"""
    reset_token = AUTH.get_reset_password_token(email)
    assert type(reset_token) == str
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    AUTH.update_password(reset_token, new_password)


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
