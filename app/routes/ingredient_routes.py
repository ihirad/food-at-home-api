from flask import Blueprint, request, abort, make_response, session
from app.models.ingredient import Ingredient
from app.models.user import Foodie
from app.models.user_ingredient import UserIngredient
from app.db import db
from app.routes.route_utilities import *
from datetime import datetime

bp = Blueprint("ingredients_bp", __name__, url_prefix="/ingredients")

@bp.post("")
def add_or_create_ingredient():
    user = get_authenticated_user(Foodie)
    ingredient_name, expiration_date = validate_and_parse_request(request)
    existing_ingredient = find_existing_ingredient(ingredient_name)
    if existing_ingredient:
        return handle_existing_ingredient(user, existing_ingredient, expiration_date)
    else:
        return handle_new_ingredient(user, ingredient_name, expiration_date)

@bp.get("")
def get_all_ingredients():
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    user_ingredients = UserIngredient.query.filter_by(foodie_id=user.id).all()
    user_ingredient_map = {ui.ingredient_id: ui for ui in user_ingredients}
    ingredient_response = []
    for ingredient in user.ingredients:
        user_ingredient = user_ingredient_map.get(ingredient.id)
        expiration_date = user_ingredient.expiration_date if user_ingredient else None
        ingredient_response.append({
            "id": ingredient.id,
            "ingredient": ingredient.ingredient,
            "expiration_date": expiration_date.isoformat() if expiration_date else None
        })
    
    return make_response({"ingredients": ingredient_response}, 200)

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