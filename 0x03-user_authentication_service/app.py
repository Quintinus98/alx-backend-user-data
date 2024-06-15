#!/usr/bin/env python3
from flask import Flask, jsonify, abort, make_response, url_for, redirect
from auth import Auth
from flask import request

app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """End-point to register a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Login function"""
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": f"{email}", "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res

    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Log out the User"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    res = make_response(redirect(url_for("home")))
    res.set_cookie("session_id", "", 0)
    return res


@app.route("/profile", methods=["GET"])
def profile():
    """Get profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return make_response(jsonify({"email": f"{user.email}"}), 200)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    email = request.form.get("email")
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return make_response(
        jsonify({"email": f"{email}", "reset_token": f"{reset_token}"}), 200
    )


@app.route("/reset_password", methods=["PUT"])
def update_password():
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return make_response(
        jsonify({"email": f"{email}", "message": "Password updated"}, 200)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
