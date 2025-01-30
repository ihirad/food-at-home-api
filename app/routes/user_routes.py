from flask import Blueprint, request, abort, make_response, session, url_for, redirect, jsonify, current_app, flash, render_template
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
# from flask_login import LoginManager, UserMixin, login_user, logout_user,login_required, current_user
# import secrets
# from urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth
from app.models.user import Foodie
from ..db import db
from app.routes.route_utilities import validate_model
from app.routes.route_utilities import *
# from app import create_app,google
from app.extensions import oauth



def init_routes(app):
    from app import create_app
    
# login_manager = LoginManager()
# login_manager.login_view = "login"

# from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user_bp", __name__, url_prefix="/users")

# GOOGLE_ID = "180858029960-h82lubscha675vsif48jhk5ao7p5ulcc.apps.googleusercontent.com"

# def verify_google_token(token):
#     """Verify Google ID Token."""
#     try:
#         id_info = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_ID)
#         return id_info  # Returns user info if valid
#     except Exception as e:
#         return None  # Invalid token

# @bp.post("/auth/google")
# def google_auth():
#     """Authenticate user using Google ID Token."""
#     token = request.json.get("id_token")
#     user_info = verify_google_token(token)

#     if not user_info:
#         return jsonify({"error": "Invalid token"}), 401

#     # Check if user exists in the database, else create one
#     user = Foodie.query.filter_by(google_id=user_info["sub"]).first()
#     if not user:
#         user = Foodie(
#             google_id=user_info["sub"],
#             email=user_info["email"],
#             name=user_info.get("name", ""),
#             picture=user_info.get("picture", "")
#         )
#         db.session.add(user)
#         db.session.commit()

#     return jsonify({
    #     "message": "Authentication successful",
    #     "user": {
    #         "user_id": user.google_id,
    #         "email": user.email,
    #         "name": user.name,
    #         "picture": user.picture,
    #     }
    # }), 200
 
# @login_manager.user_loader
# def load_user(user_id):
#     return Foodie.query.get(int(user_id))

# Google login

@bp.get("/login")
def login():
    return oauth.google.authorize_redirect(url_for("user_bp.authorize", _external=True))


# @bp.get("/authorize")
# def authorize():
#     token = oauth.google.authorize_access_token()  # Get token from Google
#     user_info = oauth.google.parse_id_token(token)  # Parse user info
#     return jsonify(user_info)  # Return user info (or create session)


# Google OAuth callback
@bp.post("/authorize")
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = token.get("userinfo")

    if not user_info:
        return "Failed to fetch user info", 400

    # Check if user exists
    user = Foodie.query.filter_by(email=user_info["email"]).first()
    
    if not user:
        user = Foodie(email=user_info["email"], name=user_info["name"])
        db.session.add(user)
        db.session.commit()

    # login_user(user)
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_email"] = user.email
    return redirect(url_for("profile"))
    return jsonify({"message": "User logged in successfully!"})

@bp.get("/profile")
def profile():
    return jsonify({"name": session["user_name"], "email": session["user_email"]})

# Read user profile (R in CRUD)
# @bp.get("/profile")
# # @login_required
# def profile():
#     return jsonify({"name": current_user.name, "email": current_user.email, "bio": current_user.bio})

# # Update user profile (U in CRUD)
# @bp.put("/profile")
# # @login_required
# def update_profile():
#     data = request.json
#     if "name" in data:
#         current_user.name = data["name"]
#     if "bio" in data:
#         current_user.bio = data["bio"]

#     db.session.commit()
#     return jsonify({"message": "Profile updated successfully!"})

# # Delete user account (D in CRUD)
# @bp.delete("/profile")
# # @login_required
# def delete_account():
#     db.session.delete(current_user)
#     db.session.commit()
#     logout_user()
#     return jsonify({"message": "Account deleted successfully!"})

# # Logout
# @bp.get("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("login"))

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()  # Ensure database is set up
#     app.run(debug=True)


# # Default route
# @bp.route('/')
# def index():
#   oauth = current_app.extensions["oauth"]
#   return render_template('index.html')


# # Google login route
# @bp.route('/login/google')
# def google_login():
#     oauth = current_app.extensions["oauth"]
#     google = oauth.create_client('google')
#     redirect_uri = url_for('google_authorize', _external=True)
#     return google.authorize_redirect(redirect_uri)


# # Google authorize route
# @bp.route('/login/google/authorize')
# def google_authorize():
#     oauth = current_app.extensions["oauth"]
#     google = oauth.create_client('google')
#     token = google.authorize_access_token()
#     resp = google.get('userinfo').json()
#     print(f"\n{resp}\n")
#     return "You are successfully signed in using google"



# # @bp.get('/authorize/<user_id>')
# # def oauth2_authorize(user_id):
#     if not current_user.is_anonymous:
#         return redirect(url_for('index'))

#     provider_data = current_app.config['OAUTH2_PROVIDERS'].get(user_id)
#     if provider_data is None:
#         abort(404)

#     # generate a random string for the state parameter
#     session['oauth2_state'] = secrets.token_urlsafe(16)

#     # create a query string with all the OAuth2 parameters
#     qs = urlencode({
#         'client_id': provider_data['client_id'],
#         'redirect_uri': url_for('oauth2_callback', provider=user_id,
#                                 _external=True),
#         'response_type': 'code',
#         'scope': ' '.join(provider_data['scopes']),
#         'state': session['oauth2_state'],
#     })

#     # redirect the user to the OAuth2 provider authorization URL
#     return redirect(provider_data['authorize_url'] + '?' + qs)

# @bp.get('/callback/<user_id>')
# def oauth2_callback(user_id):
#     if not current_user.is_anonymous:
#         return redirect(url_for('index'))

#     provider_data = current_app.config['OAUTH2_PROVIDERS'].get(user_id)
#     if provider_data is None:
#         abort(404)

#     # if there was an authentication error, flash the error messages and exit
#     if 'error' in request.args:
#         for k, v in request.args.items():
#             if k.startswith('error'):
#                 flash(f'{k}: {v}')
#         return redirect(url_for('index'))

#     # make sure that the state parameter matches the one we created in the
#     # authorization request
#     if request.args['state'] != session.get('oauth2_state'):
#         abort(401)

#     # make sure that the authorization code is present
#     if 'code' not in request.args:
#         abort(401)

#     # exchange the authorization code for an access token
#     response = requests.post(provider_data['token_url'], data={
#         'client_id': provider_data['client_id'],
#         'client_secret': provider_data['client_secret'],
#         'code': request.args['code'],
#         'grant_type': 'authorization_code',
#         'redirect_uri': url_for('oauth2_callback', user_id=user_id,
#                                 _external=True),
#     }, headers={'Accept': 'application/json'})
#     if response.status_code != 200:
#         abort(401)
#     oauth2_token = response.json().get('access_token')
#     if not oauth2_token:
#         abort(401)

#     # use the access token to get the user's email address
#     response = requests.get(provider_data['userinfo']['url'], headers={
#         'Authorization': 'Bearer ' + oauth2_token,
#         'Accept': 'application/json',
#     })
#     if response.status_code != 200:
#         abort(401)
#     email = provider_data['userinfo']['email'](response.json())

#     # find or create the user in the database
#     user = db.session.scalar(db.select(Foodie).where(Foodie.email == email))
#     if user is None:
#         user = Foodie(email=email, username=email.split('@')[0])
#         db.session.add(user)
#         db.session.commit()

#     # log the user in
#     login_user(user)
#     return redirect(url_for('index'))

# @bp.post("/register")
# def register_user():
#     request_body = request.get_json()
#     if "username" not in request_body or "password" not in request_body:
#         abort(make_response({"message": "Missing username or password"}, 400))
#     if not request_body["username"] or not request_body["password"]:
#         abort(make_response({"message": "Invalid username or password"}, 400))
#     username = request_body["username"]
#     password = request_body["password"]
#     foodie = Foodie(username=username, password=generate_password_hash(password))
#     db.session.add(foodie)
#     db.session.commit()
#     return make_response({"message": f"User {foodie.id} created"}, 201)

# @bp.post("/login")
# def login_user():
#     request_body = request.get_json()
#     if "username" not in request_body or "password" not in request_body:
#         abort(make_response({"message": "Missing username or password"}, 400))
#     if not request_body["username"] or not request_body["password"]:
#         abort(make_response({"message": "Invalid username or password"}, 400))
    
#     username = request_body["username"]
#     password = request_body["password"]
    
#     foodie = Foodie.query.filter_by(username=username).first()
#     if not foodie or not foodie.check_password(password):
#         abort(make_response({"message": "Invalid username or password"}, 401))
#     session["user_id"] = foodie.id
    # return make_response({"message": f"User {foodie.id} logged in"}, 200)

# @bp.post('/register')
# def register_user():
#     data = request.get_json()
#     if not data.get('username') or not data.get('password'):
#         return jsonify({"message": "Missing username or password"}), 400

#     if Foodie.query.filter_by(username=data['username']).first():
#         return jsonify({"message": "Username already taken"}), 400

#     user = Foodie(username=data['username'], password=data['password'])
#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"message": "User created successfully"}), 201


# @bp.route('/')
# def index():
#     return 'Welcome to the OAuth 2.0 Flask App'

# @bp.route('/login')
# def login():
#     return google.authorize(callback=url_for('authorized', _external=True))


# @bp.route('/login/authorized')
# def authorized():
#     response = google.authorized_response()
#     if response is None or response.get('access_token') is None:
#         return 'Access denied: reason={} error={}'.format(
#             request.args['error_reason'],
#             request.args['error_description']
#         )

#     session['google_token'] = (response['access_token'], '')
#     user_info = google.get('userinfo')

# @bp.get('/me')
# def get_user_details():
#     user_id = session.get('user_id')

#     if not user_id:
#         return jsonify({"message": "User not logged in"}), 401

#     user = Foodie.query.get(user_id)
#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     return jsonify(user.to_dict()), 200

# @bp.post('/login')
# def login():
#     data = request.get_json()
#     user = Foodie.query.filter_by(username=data['username']).first()

#     if not user or not check_password_hash(user.password, data['password']):
#         return jsonify({"message": "Invalid credentials"}), 401

#     session['user_id'] = user.id  # Store user ID in the session
#     return jsonify({"message": "Login successful"}), 200

# @bp.get('/authorized')
# def authorized():
#     response = google.authorized_response()
#     if response is None or response.get('access_token') is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['google_token'] = (response['access_token'], '')
#     user_info = google.get('userinfo')
#     return jsonify(user_info.data)

# @bp.get('/')
# def index():
#     return "Welcome to the OAuth 2.0 Flask App!"

# @bp.get('/login')
# def login():
#     redirect_uri = url_for('user_bp.authorized', _external=True)
#     return google.authorize_redirect(redirect_uri)

# @bp.get('/logout')
# def logout():
#     session.pop('google_token', None)
#     return redirect(url_for('index'))

# @google.tokengetter
# def get_google_oauth_token():
#     return session.get('google_token')

          

# @bp.post("/register")
# def register_user():
#     request_body = request.get_json()
#     if "username" not in request_body or "password" not in request_body:
#         abort(make_response({"message": "Missing username or password"}, 400))
#     if not request_body["username"] or not request_body["password"]:
#         abort(make_response({"message": "Invalid username or password"}, 400))
#     username = request_body["username"]
#     password = request_body["password"]
#     foodie = Foodie(username=username, password=generate_password_hash(password))
#     db.session.add(foodie)
#     db.session.commit()
#     return make_response({"message": f"User {foodie.id} created"}, 201)

# @bp.post("/login")
# def login_user():
#     request_body = request.get_json()
#     if "username" not in request_body or "password" not in request_body:
#         abort(make_response({"message": "Missing username or password"}, 400))
#     if not request_body["username"] or not request_body["password"]:
#         abort(make_response({"message": "Invalid username or password"}, 400))
    
#     username = request_body["username"]
#     password = request_body["password"]
    
#     foodie = Foodie.query.filter_by(username=username).first()
#     if not foodie or not foodie.check_password(password):
#         abort(make_response({"message": "Invalid username or password"}, 401))
#     session["user_id"] = foodie.id
#     return make_response({"message": f"User {foodie.id} logged in"}, 200)

# @bp.get("/logout")
# def logout_user():
#     session.pop("user_id")
#     return make_response({"message": "User logged out"}, 200)

# @bp.delete("/<user_id>")
# def delete_user(user_id):
#     user = validate_model(Foodie, user_id)
#     db.session.delete(user)
#     db.session.commit()
#     return make_response({"message": f"User {user_id} deleted"}, 200)

