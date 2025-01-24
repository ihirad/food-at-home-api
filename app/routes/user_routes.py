from flask import Blueprint,request,abort,make_response
from app.models.user import Foodie
from ..db import db
from .route_utilities import validate_model
from app.routes.route_utilities import *
from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash

bp = Blueprint("user_bp", __name__, url_prefix="/users")

@bp.post("/register")
def register_user():
    request_body = request.get_json()
    if "username" not in request_body or "password" not in request_body:
        abort(make_response({"message": "Missing username or password"}, 400))
    if not request_body["username"] or not request_body["password"]:
        abort(make_response({"message": "Invalid username or password"}, 400))
    username = request_body["username"]
    password = request_body["password"]
    foodie = Foodie(username=username, password=generate_password_hash(password))
    db.session.add(foodie)
    db.session.commit()
    return make_response({"message": f"User {foodie.id} created"}, 201)

@bp.post("/login")
def login_user():
    request_body = request.get_json()
    if "username" not in request_body or "password" not in request_body:
        abort(make_response({"message": "Missing username or password"}, 400))
    if not request_body["username"] or not request_body["password"]:
        abort(make_response({"message": "Invalid username or password"}, 400))
    username = request_body["username"]
    password = request_body["password"]
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or not user.check_password(password):
        abort(make_response({"message": "Invalid username or password"}, 400))
    session["user_id"] = user.id
    return make_response({"message": f"User {user.id} logged in"}, 200)

@bp.get("/logout")
def logout_user():
    session.pop("user_id")
    return make_response({"message": "User logged out"}, 200)

@bp.delete("/<user_id>")
def delete_user(user_id):
    user = validate_model(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return make_response({"message": f"User {user_id} deleted"}, 200)