from flask import Flask
from flask_cors import CORS
import os
from .db import db, migrate
from .models import shopping_note, user, user_ingredient, recipe, ingredient
from .routes.ingredient_routes import bp as ingredient_bp
from .routes.shopping_note_routes import bp as shopping_note_bp
from .routes.proxy_routes import bp as proxy_bp
from .routes.user_routes import bp as user_bp
from .routes.recipe_routes import bp as recipe_bp
from dotenv import load_dotenv



def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    load_dotenv()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.secret_key = os.environ.get('SECRET_KEY')
    app.SPOONACULAR_ID = os.getenv("SPOONACULAR_ID")

    if config:
        app.config.update(config)

    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(ingredient_bp)
    app.register_blueprint(shopping_note_bp)
    app.register_blueprint(proxy_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(recipe_bp)
    return app
