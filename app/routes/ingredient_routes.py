from flask import Blueprint, request, abort, make_response
from app.models.ingredient import Ingredient
from app.models.user import User
from app.models.shopping_note import ShoppingNote
from app.db import db
from app.routes.route_utilities import *


bp = Blueprint("ingredients_bp", __name__, url_prefix="/ingredients")