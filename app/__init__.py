from flask import Flask,redirect, url_for,session,render_template
from flask_cors import CORS
import os
from .db import db, migrate
from .models import shopping_note, user, ingredient, recipe, ingredient, user_ingredient
from .routes.ingredient_routes import bp as ingredient_bp
from .routes.shopping_note_routes import bp as shopping_note_bp
from .routes.user_routes import bp as user_bp
from .routes.recipe_routes import bp as recipe_bp
from dotenv import load_dotenv
# from authlib.integrations.flask_client import OAuth
from app.extensions import oauth
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# from flask_login import LoginManager

# login_manager = LoginManager()
# login_manager.login_view = "login"




def create_app(config=None):
    app = Flask(__name__)
    oauth.init_app(app)
    CORS(app)
    load_dotenv()
    # login_manager.init_app(app)

    

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # app.secret_key = os.environ.get('SECRET_KEY')
    app.SPOONACULAR_ID = os.getenv("SPOONACULAR_ID")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['GOOGLE_ID'] = os.getenv("GOOGLE_ID")
    if config:
        app.config.update(config)

    # google = oauth.register(
    #     name='google',
    #     client_id=app.config["GOOGLE_ID"],
    #     client_secret=None,
    #     access_token_url='https://accounts.google.com/o/oauth2/token',
    #     access_token_params=None,
    #     authorize_url='https://accounts.google.com/o/oauth2/auth',
    #     authorize_params={"scope": "openid email profile"},
    #     api_base_url='https://www.googleapis.com/oauth2/v1/',
    #     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    #     client_kwargs={'scope': 'openid email profile'},
    #     redirect_uri='http://localhost:5000/google-login'
    # )


    # google = oauth.register(
    #     name='google',
    #     client_id=app.config['GOOGLE_ID'],
    #     client_secret=None,
    #     request_token_params={
    #         'scope': 'email',
    #     },
    #     base_url='https://www.googleapis.com/oauth2/v1/',
    #     refresh_token_url=None,
    #     access_token_method='POST',
    #     access_token_url='https://accounts.google.com/o/oauth2/token',
    #     authorize_url='https://accounts.google.com/o/oauth2/auth',
        
    # )
    


    # def get_google_oauth_token():
    #     return session.get('google_token')
    # login_manager.login_view = 'login'

    # def authorized(response):
    #     if response:
    #         session['google_token'] = response['access_token']
    #     return redirect(url_for('index'))

  
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(ingredient_bp)
    app.register_blueprint(shopping_note_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(recipe_bp)



    if __name__ == '__main__':
        app.run(debug=True)


    # def load_user(user_id):
    #     return Foodie.query.get(int(user_id))

    return app
