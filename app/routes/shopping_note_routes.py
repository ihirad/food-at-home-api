from flask import Blueprint, request, abort, make_response
from app.models.ingredient import Ingredient
from app.models.user import Foodie
from app.models.shopping_note import ShoppingNote
from app.db import db
from app.routes.route_utilities import *

bp = Blueprint("note_bp", __name__, url_prefix="/notes")

@bp.post("/<user_id>")
def create_note(user_id):
    user = validate_model(User, user_id)
    request_body = request.get_json()
    request_body["user_id"] = user.id
    return create_model(ShoppingNote, request_body)

@bp.get("/<user_id>")
def get_all_notes(user_id):
    user = validate_model(User, user_id)
    filters = dict(request.args)
    filters["user_id"] = user.id
    return get_models_with_filters(ShoppingNote, filters)


@bp.put("/<note_id>/<user_id>")
def update_note(note_id, user_id):
    user = validate_model(User, user_id)
    shopping_note = validate_model(ShoppingNote, note_id)
    if shopping_note.user_id != user.id:
        abort(make_response({"message": f"Note {note_id} does not belong to user {user_id}"}, 400))
    request_body = request.get_json()
    shopping_note.note = request_body["note"]
    db.session.commit()
    response = {shopping_note.to_dict()}
    return response


@bp.delete("/<note_id>/<user_id>")
def delete_note(note_id, user_id):
    user = validate_model(User, user_id)
    shopping_note = validate_model(ShoppingNote, note_id)
    if shopping_note.user_id != user.id:
        abort(make_response({"message": f"Note {note_id} does not belong to user {user_id}"}, 400))
    db.session.delete(shopping_note)
    db.session.commit()
    return make_response({"message": f"Note {note_id} deleted"}, 200)