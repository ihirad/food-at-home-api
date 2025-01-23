from flask import Flask
from flask_cors import CORS
import os
from .db import db, migrate
from .routes.ingredient_routes import bp as ingredient_bp
from .routes.shopping_note_routes import bp as shopping_note_bp
from .routes.proxy_routes import bp as proxy_bp
from .models import Ingredient, ShoppingNote, UserIngredient, User


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(ingredient_bp)
    app.register_blueprint(shopping_note_bp)
    app.register_blueprint(proxy_bp)

    return app
