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
    """Add or update an ingredient for the logged-in user"""
    user = get_authenticated_user()
    ingredient_name, expiration_date = validate_and_parse_request(request)
    existing_ingredient = find_existing_ingredient(ingredient_name)
    if existing_ingredient:
        return handle_existing_ingredient(user, existing_ingredient, expiration_date)
    else:
        return handle_new_ingredient(user, ingredient_name, expiration_date)
    
# @bp.post("")
# def add_or_create_ingredient():
#     user_id = get_logged_in_user()
#     user = validate_model(Foodie, user_id)
    
#     request_body = request.get_json()
#     ingredient_name = request_body.get("ingredient")
#     expiration_date_str = request_body.get("expirationDate")  # Expecting "YYYY-MM-DD" or None

#     if not ingredient_name:
#         abort(make_response({"message": "Missing required field: 'ingredient'"}, 400))
        
#     query = db.select(Ingredient).where(Ingredient.ingredient == ingredient_name)
#     existing_ingredient = db.session.scalar(query)

#     expiration_date = None
#     if expiration_date_str:
#         try:
#             expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
#         except ValueError:
#             abort(make_response({"message": "Invalid expirationDate format. Use YYYY-MM-DD."}, 400))
    
#     if existing_ingredient:
#         association = (
#             db.session.query(UserIngredient)
#             .filter_by(foodie_id=user.id, ingredient_id=existing_ingredient.id)
#             .first()
#         )
#         if association:
#             if expiration_date is not None:
#                 association.expiration_date = expiration_date
#                 db.session.commit()
#         else:
#             new_assoc = UserIngredient(
#                 foodie_id=user.id,
#                 ingredient_id=existing_ingredient.id,
#                 expiration_date=expiration_date
#             )
#             db.session.add(new_assoc)
#             db.session.commit()
            
#         return make_response({
#             "message": f"Ingredient '{ingredient_name}' updated",
#             "ingredient": existing_ingredient.to_dict()
#         }, 200)
    
#     else:
#         new_ingredient = Ingredient(ingredient=ingredient_name)
#         db.session.add(new_ingredient)
#         db.session.commit()  
        
#         new_assoc = UserIngredient(
#             foodie_id=user.id,
#             ingredient_id=new_ingredient.id,
#             expiration_date=expiration_date
#         )
#         db.session.add(new_assoc)
#         db.session.commit()

#         return make_response({
#             "message": f"Ingredient '{ingredient_name}' created and added to user",
#             "ingredient": new_ingredient.to_dict()
#         }, 201)


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