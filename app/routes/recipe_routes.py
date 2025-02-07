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
def get_recipe_by_ingredients():
    include_ingredients = request.args.get("includeIngredients", default="", type=str)
    if include_ingredients:
        ingredients_list = [ingredient.strip() for ingredient in include_ingredients.split(",")]
        include_ingredients = ",".join(ingredients_list)
    print("SpoonacularID is :", SPOONACULAR_ID)
    try:
        response = requests.get(
            "https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": SPOONACULAR_ID,
                "query": "",  
                "includeIngredients": include_ingredients,
                "number": 2,
                "addRecipeInformation": True,
                "addRecipeInstructions": True,
                "fillIngredients": True
            }
        )
        if response.status_code != 200:
            abort(make_response(
                {"message": "Recipe did not load, try again later."},
                response.status_code
            ))

        data = response.json()
        results = data.get("results", [])
        selected_recipes = [extract_recipe_data(recipe) for recipe in results]
        return make_response({"recipes": selected_recipes}, 200)
    
    except requests.exceptions.RequestException as e:
        abort(make_response(
            {"message": "An error occurred while getting recipe", "error": str(e)},
            500
        ))


@bp.get("/<recipe_id>")
def get_recipe_by_id(recipe_id):
    recipe_id = int(recipe_id)
    if not recipe_id:
        return make_response({"message": "Please provide a valid recipe id"}, 400)
    try:
        response = requests.get(
            f"https://api.spoonacular.com/recipes/{recipe_id}/information",
            params={
                "apiKey": SPOONACULAR_ID,
                "includeNutrition": "false",
                "addRecipeInformation": "true",
                "addRecipeInstructions": "true",
                "fillIngredients": "true"
            }
        )
        if response.status_code != 200:
            abort(make_response({"message": "Failed to fetch recipe information"}, response.status_code))
        recipe = response.json()
        return make_response({"recipes": extract_recipe_data(recipe)}, 200)

        # results = recipe.get("recipe", [])
        # selected_recipes = [extract_recipe_data(recipe) for recipe in results]
        # return make_response({"recipes": selected_recipes}, 200)
        # return make_response({"recipe": recipe}, 200)
    except requests.exceptions.RequestException as e:
        abort(make_response({"message": "An error occurred while fetching recipe information", "error": str(e)}, 500))

@bp.post("")
def save_recipe():
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    request_body = request.get_json()
    request_body["foodie_id"] = user.id
    return create_model(Recipe, request_body)

@bp.get("/all")
def get_all_recipes():
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    filters = dict(request.args)
    filters["foodie_id"] = user.id
    return get_models_with_filters(Recipe, filters)

@bp.delete("/<recipe_id>")
def delete_recipe(recipe_id):
    user_id = get_logged_in_user()
    user = validate_model(Foodie, user_id)
    recipe = validate_model(Recipe, recipe_id)
    if recipe.foodie_id != user.id:
        abort(make_response({"message": f"Recipe {recipe_id} does not belong to user {user_id}"}, 400))
    db.session.delete(recipe)
    db.session.commit()
    return make_response({"message": f"Recipe {recipe_id} deleted"}, 200)