from flask import Flask,redirect, url_for,session,render_template
from flask_cors import CORS
import os
from .db import db, migrate
from .models import shopping_note, user, ingredient, recipe, ingredient, user_ingredient
from .routes.ingredient_routes import bp as ingredient_bp
from .routes.shopping_note_routes import bp as shopping_note_bp
from .routes.user_routes import bp as user_bp
from .routes.recipe_routes import bp as recipe_bp
from .routes.user_ingredient_route import bp as user_ingredient_bp
from dotenv import load_dotenv


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    load_dotenv()
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    app.SPOONACULAR_ID = os.getenv("SPOONACULAR_ID")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    # app.config['GOOGLE_ID'] = os.getenv("GOOGLE_ID")
    if config:
        app.config.update(config)

    
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(ingredient_bp)
    app.register_blueprint(shopping_note_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(user_ingredient_bp)

    if __name__ == '__main__':
        app.run(debug=True)

    

    return app
