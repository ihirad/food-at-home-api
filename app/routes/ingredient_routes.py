from flask import Blueprint, request, abort, make_response
from app.models.ingredient import Ingredient
from app.models.user import User
from app.models.shopping_note import ShoppingNote
from app.db import db
from app.routes.route_utilities import *


bp = Blueprint("ingredients_bp", __name__, url_prefix="/ingredients")

# @bp.post("")
# def post_ingredient():
#     request_body = request.get_json()
#     ingredient_name = request_body.get("name")
#     if not ingredient_name:
#         abort(make_response({"message": "Missing required field: 'name'"}, 400))
#     # query = db.select(Ingredient).where(Ingredient.name == ingredient_name)
#     # existing_ingredient = db.session.scalar(query)

#     existing_ingredient = db.session.query(Ingredient).filter_by(name=ingredient_name).first()

#     if existing_ingredient:
#         return make_response({
#             "message": f"Ingredient '{ingredient_name}' already exists",
#             "ingredient": existing_ingredient.to_dict()
#         }, 200)

#     return create_model(Ingredient, {"name": ingredient_name})


@bp.post("/<user_id>/ingredients")
def add_or_create_ingredient(user_id):
    user = validate_model(User, user_id)
    request_body = request.get_json()
    ingredient_name = request_body.get("name")
    
    if not ingredient_name:
        abort(make_response({"message": "Missing required field: 'name'"}, 400))
        
    query = db.select(Ingredient).where(Ingredient.name == ingredient_name)
    existing_ingredient = db.session.scalar(query)

    if existing_ingredient:
        if user not in existing_ingredient.user:
            existing_ingredient.user.append(user)
            db.session.commit()
        return make_response({
            "message": f"Ingredient '{ingredient_name}' updated",
            "ingredient": existing_ingredient.to_dict()
        }, 200)
    else:
        new_ingredient_data = {
            "name": ingredient_name,
            "users": [{"id": user.id}]
        }
        return create_model(Ingredient, new_ingredient_data)

@bp.get("/<user_id>")
def get_all_ingredients(user_id):
    user = validate_model(User, user_id)
    ingredients = user.ingredients 
    return make_response({
        "ingredients": [ingredient.to_dict() for ingredient in ingredients]
    }, 200)