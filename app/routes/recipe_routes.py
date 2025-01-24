from flask import Blueprint,request,abort,make_response
from app.models.user import User
from app.models.recipe import Recipe
from ..db import db
from .route_utilities import validate_model
from app.routes.route_utilities import *
import requests


bp = Blueprint("user_bp", __name__, url_prefix="/recipes")


@bp.get("/")
def get_recipes():
    
    ingredients = request.args.get("ingredients")
    
    if not ingredients:
        return make_response({"message": "Please provide a list of ingredients"}, 400)

    try:
        response = requests.get(
            "https://api.spoonacular.com/recipes/findByIngredients",
            params={
                "apiKey": "000",  
                "number": 10,
                "ingredients": ingredients
            }
        )
        
        if response.status_code != 200:
            abort(make_response({"message": "Failed to fetch recipes"}, response.status_code))
        
        recipes = response.json()  
        return make_response({"recipes": recipes}, 200)

    except requests.exceptions.RequestException as e:
        abort(make_response({"message": "An error occurred while fetching recipes", "error": str(e)}, 500))

@bp.post("/save")
def save_recipe():
    request_data = request.get_json()

    if not request_data or "name" not in request_data or "spoonacularid" not in request_data or "userid" not in request_data:
        return make_response({"message": "Invalid data"}, 400)
    
    new_recipe = Recipe.from_dict(request_data)
    
    try:
        db.session.add(new_recipe)
        db.session.commit()
        return make_response({"message": "Recipe saved successfully"}, 201)
    except Exception as e:
        db.session.rollback()
        return make_response({"message": "An error occurred while saving the recipe", "error": str(e)}, 500)
    
@bp.get("/<user_id>")
def get_all_recipes(user_id):
    user = validate_model(User, user_id)
    recipes = db.session.execute(db.select(Recipe).where(Recipe.userid == user_id)).scalars().all()
    return make_response({"recipes": [recipe.to_dict() for recipe in recipes]}, 200)

@bp.delete("/<recipe_id>")
def delete_recipe(recipe_id):
    recipe = validate_model(Recipe, recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return make_response({"message": f"Recipe {recipe_id} deleted"}, 200)