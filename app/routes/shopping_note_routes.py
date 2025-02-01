from flask import Blueprint, request, abort, make_response
from app.models.user import Foodie
from app.models.shopping_note import ShoppingNote
from app.db import db
from app.routes.route_utilities import *

bp = Blueprint("note_bp", __name__, url_prefix="/notes")

@bp.post("")
def create_note():
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    request_body = request.get_json()
    request_body["foodie_id"] = user.id
    new_note = create_model(ShoppingNote, request_body)
    return new_note

# @bp.get("")
# def get_all_notes():
#     user_id = get_logged_in_user()
#     user = validate_model(Foodie, user_id)
#     notes = user.shopping_notes
#     note_response = [
#         {
#             "id": note.id,
#             "note": note.name
#         }
#         for note in notes
#     ]
#     return make_response({"notes": note_response}, 200)

@bp.get("")
def get_all_notes():
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    filters = dict(request.args)
    filters["foodie_id"] = user.id
    return get_models_with_filters(ShoppingNote, filters)


@bp.put("/<note_id>")
def update_note(note_id):
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    shopping_note = validate_model(ShoppingNote, note_id)
    if shopping_note.foodie_id != user.id:
        abort(make_response({"message": f"Note {note_id} does not belong to user {user_id}"}, 400))
    request_body = request.get_json()
    shopping_note.note = request_body["note"]
    db.session.commit()
    response = shopping_note.to_dict()
    return response


@bp.delete("/<note_id>")
def delete_note(note_id):
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    shopping_note = validate_model(ShoppingNote, note_id)
    if shopping_note.foodie_id != user.id:
        abort(make_response({"message": f"Note {note_id} does not belong to user {user_id}"}, 400))
    db.session.delete(shopping_note)
    db.session.commit()
    return make_response({"message": f"Note {note_id} deleted"}, 200)