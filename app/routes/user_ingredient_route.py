from flask import Blueprint, request, abort, make_response, session
from app.models.ingredient import Ingredient
from app.models.user import Foodie
from app.models.user_ingredient import UserIngredient
from app.db import db
from app.routes.route_utilities import *

bp = Blueprint("user_ingredients_bp", __name__, url_prefix="/useringredients")

@bp.put("/<ingredient_id>")
def update_expiration_date(ingredient_id):
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    
    request_body = request.get_json()
    # ingredient_id = request_body.get("ingredient_id")
    expiration_date = request_body.get("expiration_date")
    
    if not ingredient_id or not expiration_date:
        abort(make_response({"message": "Missing required fields: 'ingredient_id' or 'expiration_date'"}, 400))#4xx
    
    ingredient = validate_model(Ingredient, ingredient_id)
        
    query = db.select(UserIngredient).where(UserIngredient.ingredient_id == ingredient.id and UserIngredient.foodie_id == user.id)
    user_ingredient = db.session.scalar(query)
    if user_ingredient:
        user_ingredient.expiration_date = expiration_date
        db.session.commit()
        return make_response({"message": f"Expiration date for ingredient {ingredient.id} updated to {expiration_date}"}, 200) 
    else:
        abort(make_response({"message": f"User {user.id} does not have ingredient {ingredient.id}"}, 400))