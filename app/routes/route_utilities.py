from flask import abort, make_response, request, session
from ..db import db
from ..models.ingredient import Ingredient
from ..models.shopping_note import ShoppingNote
from ..models.user import Foodie
from ..models.recipe import Recipe
from app.models.user_ingredient import UserIngredient
from datetime import datetime

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

def get_authenticated_user():
    """Validate and return the logged-in user"""
    user_id = get_logged_in_user()
    return validate_model(Foodie, user_id)

def validate_and_parse_request(request):
    """Validate request and parse expiration date"""
    request_body = request.get_json()
    ingredient_name = request_body.get("ingredient")
    expiration_date_str = request_body.get("expirationDate")

    if not ingredient_name:
        abort(make_response({"message": "Missing required field: 'ingredient'"}, 400))

    expiration_date = None
    if expiration_date_str:
        try:
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
        except ValueError:
            abort(make_response({"message": "Invalid expirationDate format. Use YYYY-MM-DD."}, 400))

    return ingredient_name, expiration_date

def find_existing_ingredient(ingredient_name):
    """Check if ingredient already exists in database"""
    return db.session.scalar(
        db.select(Ingredient).where(Ingredient.ingredient == ingredient_name)
    )

def handle_existing_ingredient(user, ingredient, expiration_date):
    """Handle existing ingredient user association"""
    association = get_user_ingredient_association(user.id, ingredient.id)
    
    if association:
        update_existing_association(association, expiration_date)
        message = f"Ingredient '{ingredient.ingredient}' updated"
    else:
        create_user_ingredient_association(user.id, ingredient.id, expiration_date)
        message = f"Ingredient '{ingredient.ingredient}' added to user"

    return make_response({
        "message": message,
        "ingredient": ingredient.to_dict()
    }, 200)

def handle_new_ingredient(user, ingredient_name, expiration_date):
    """Create new ingredient and user association"""
    new_ingredient = create_ingredient(ingredient_name)
    create_user_ingredient_association(user.id, new_ingredient.id, expiration_date)
    
    return make_response({
        "message": f"Ingredient '{ingredient_name}' created and added to user",
        "ingredient": new_ingredient.to_dict()
    }, 201)

def get_user_ingredient_association(user_id, ingredient_id):
    """Get existing user-ingredient association"""
    return db.session.query(UserIngredient).filter_by(
        foodie_id=user_id,
        ingredient_id=ingredient_id
    ).first()

def update_existing_association(association, expiration_date):
    """Update expiration date on existing association"""
    if expiration_date is not None:
        association.expiration_date = expiration_date
        db.session.commit()

def create_user_ingredient_association(user_id, ingredient_id, expiration_date):
    """Create new user-ingredient association"""
    new_assoc = UserIngredient(
        foodie_id=user_id,
        ingredient_id=ingredient_id,
        expiration_date=expiration_date
    )
    db.session.add(new_assoc)
    db.session.commit()

def create_ingredient(ingredient_name):
    """Create new ingredient in database"""
    new_ingredient = Ingredient(ingredient=ingredient_name)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient
