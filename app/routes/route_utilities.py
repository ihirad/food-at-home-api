from flask import abort, make_response, request, session
from ..db import db
from ..models.ingredient import Ingredient
from ..models.shopping_note import ShoppingNote
from ..models.user import Foodie
from ..models.recipe import Recipe

def get_logged_in_user():
    user_id = session.get("user_id")
    if not user_id:
        abort(make_response({"message": "User not logged in"}, 401))
    return user_id

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError: 
        abort(make_response({"message":f"{cls.__name__} id {model_id} is invalid"}, 400))
    
    id_mapping = {
        Ingredient: Ingredient.id,
        ShoppingNote: ShoppingNote.id,
        Foodie: Foodie.id,
        Recipe: Recipe.id
    }

    if cls not in id_mapping:
        abort(make_response({"message": f"Invalid model type: {cls.__name__}"}, 400))
        
    query = db.select(cls).where(id_mapping[cls] == model_id)
    model = db.session.scalar(query)
    if not model:
        abort(make_response({"message":f"{cls.__name__} id {model_id} is not found"}, 404))
    return model

def create_model(cls, model_data): 
    try: 
        new_model = cls.from_dict(model_data) 
    except KeyError as error: 
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))        
    db.session.add(new_model) 
    db.session.commit()
    return make_response({f"{cls.__name__.lower()}": new_model.to_dict()}, 201)

def get_models_with_filters(cls, filters): 
    query = db.select(cls)
    for key, value in filters.items():
        query = query.where(getattr(cls, key) == value)
    models = db.session.execute(query).scalars().all()
    return make_response({f"{cls.__name__.lower()}": [model.to_dict() for model in models]}, 200)

def extract_recipe_data(recipe):
    extended_ingredients = [
        {
            "nameClean": ing.get("nameClean"),
            "original": ing.get("original"),
            "amount": ing.get("amount"),
            "unit": ing.get("unit")
        }
        for ing in recipe.get("extendedIngredients", [])
    ]
    
    instructions = []
    for instruction in recipe.get("analyzedInstructions", []):
        for step in instruction.get("steps", []):
            instructions.append(step.get("step"))
    
    missed_ingredients = [
        ing.get("original") for ing in recipe.get("missedIngredients", [])
    ]  

    return {
        "id": recipe.get("id"),
        "title": recipe.get("title"),
        "image": recipe.get("image"),
        "readyInMinutes": recipe.get("readyInMinutes"),
        "servings": recipe.get("servings"),
        "extendedIngredients": extended_ingredients,
        "instructions": instructions,
        "missedIngredients": missed_ingredients,
        "summary": recipe.get("summary")
    }
