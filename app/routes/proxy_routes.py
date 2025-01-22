from flask import Blueprint, request
import os
from dotenv import load_dotenv
import requests

load_dotenv()

bp = Blueprint("proxy_bp", __name__)

recipe_key = os.environ.get("RECIPE_KEY")

@bp.get("/recipes")
def get_recipe():
    pass

@bp.get("/recipe")
def get_recipe_by_ingredient():
    pass