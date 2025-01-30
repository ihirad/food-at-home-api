from flask import Blueprint, request, abort, make_response, session
from app.models.ingredient import Ingredient
from app.models.user import Foodie
from app.models.shopping_note import ShoppingNote
from app.db import db
from app.routes.route_utilities import *

bp = Blueprint("ingredients_bp", __name__, url_prefix="/ingredients")

@bp.post("")
def add_or_create_ingredient():
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    
    request_body = request.get_json()
    ingredient_name = request_body.get("name")
    if not ingredient_name:
        abort(make_response({"message": "Missing required field: 'name'"}, 400))
        
    query = db.select(Ingredient).where(Ingredient.name == ingredient_name)
    existing_ingredient = db.session.scalar(query)

    if existing_ingredient:
        if user not in existing_ingredient.foodies:
            existing_ingredient.foodies.append(user)
            db.session.commit()
        return make_response({
            "message": f"Ingredient '{ingredient_name}' updated",
            "ingredient": existing_ingredient.to_dict()
        }, 200)
    else:
        new_ingredient = Ingredient(name=ingredient_name)
        new_ingredient.foodies.append(user)  # Associate it with the Foodie
        db.session.add(new_ingredient)
        db.session.commit()

        return make_response({
            "message": f"Ingredient '{ingredient_name}' created and added to user",
            "ingredient": new_ingredient.to_dict()
        }, 201)

@bp.get("")
def get_all_ingredients():
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    ingredients = user.ingredients
    ingredient_response = [
        {
            "id": ingredient.id,
            "ingredient": ingredient.name
        }
        for ingredient in ingredients
    ]
    return make_response({"ingredients": ingredient_response}, 200)
# @bp.get("")
# def get_all_ingredients():
#     user_id = get_logged_in_user()
#     user = validate_model(Foodie, user_id)
#     ingredients = user.ingredients
#     ingredient_names = [ingredient.name for ingredient in ingredients]
#     return make_response({"ingredients": ingredient_names}, 200)

@bp.delete("/<ingredient_id>")
def delete_ingredient(ingredient_id):
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    ingredient = validate_model(Ingredient, ingredient_id)
    if user not in ingredient.foodies:
        abort(make_response({"message": f"Ingredient {ingredient_id} does not belong to user {user_id}"}, 400))
    ingredient.foodies.remove(user)
    db.session.commit()
    return make_response({"message": f"Ingredient {ingredient_id} deleted"}, 200)