#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - Login a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 400
    user = users[0]  # email is unique
    if not User.is_valid_password(user, password):
        return jsonify({"error": "wrong password"})

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    SESSION_NAME = os.getenv("SESSION_NAME")
    res = jsonify(user.to_json())
    res.set_cookie(SESSION_NAME, session_id)

    return res
