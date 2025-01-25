from flask import Blueprint, request, abort, make_response, session
from app.models.user import Foodie
from app.models.recipe import Recipe
from ..db import db
from .route_utilities import validate_model
from app.routes.route_utilities import *
import requests
from dotenv import load_dotenv
import os

load_dotenv()
SPOONACULAR_ID = os.getenv("SPOONACULAR_ID")



bp = Blueprint("recipe_bp", __name__, url_prefix="/recipes")


@bp.get("/")
def get_recipes():
    
    ingredients = request.args.get("ingredients")
    
    if not ingredients:
        return make_response({"message": "Please provide a list of ingredients"}, 400)

    try:
        response = requests.get(
            "https://api.spoonacular.com/recipes/findByIngredients",
            params={
                "apiKey": SPOONACULAR_ID,  
                "number": 10,
                "ingredients": ingredients
            }
        )
        
        if response.status_code != 200:
            abort(make_response({"message": "Failed to fetch recipes"}, response.status_code))
        
        recipes = response.json()  
        
        filtered_recipes = [
            {"id": recipe["id"], "name": recipe["title"], "image": recipe["image"]}
            for recipe in recipes
        ]
        return make_response({"recipes": filtered_recipes}, 200)
    except requests.exceptions.RequestException as e:
        abort(make_response({"message": "An error occurred while fetching recipes", "error": str(e)}, 500))


@bp.post("/")
def create_recipe():
    request_body = request.get_json()

    try:
        new_recipe = Recipe.from_dict(request_body)
     
    except KeyError:
        response = {"details":f"Invalid data"}
        abort(make_response(response,400))


    db.session.add(new_recipe)
    db.session.commit()

    response = new_recipe.to_dict()

    return response,201

@bp.get("/all")
def get_all_recipes():
    try:
        query = db.select(Recipe).order_by(Recipe.id)
        recipes = db.session.scalars(query).all()

        recipes_response = [recipe.to_dict() for recipe in recipes]
        return recipes_response, 200
    except Exception as e:
        print(f"Error fetching recipes: {e}")  
        return {"error": "An error occurred while fetching recipes."}, 500

@bp.delete("/<recipe_id>")
def delete_recipe(recipe_id):
    recipe = validate_model(Recipe, recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return make_response({"message": f"Recipe {recipe_id} deleted"}, 200)