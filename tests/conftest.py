import sys
import os
import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.user import Foodie
from werkzeug.security import generate_password_hash

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    user = Foodie(username="testuser", password=generate_password_hash("testpassword"))
    db.session.add(user)
    db.session.commit()

    
    login_response = client.post("/users/login", json={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200  

    return client  

@pytest.fixture
def two_saved_recipes(app):
    recipe_1 = {
    "recipes": {
        "extendedIngredients": [
            {
                "amount": 1.0,
                "nameClean": "boquerones",
                "original": "1 lb whole fresh, or cleaned and marinated anchovies (not the salted or tinned variety)",
                "unit": "lb"
            },
            {
                "amount": 0.25,
                "nameClean": "ground cayenne pepper",
                "original": "0.25 t cayenne pepper",
                "unit": "t"
            },
            {
                "amount": 0.0,
                "nameClean": "cherry tomato",
                "original": "0 cherry tomatoes, as needed",
                "unit": ""
            },
            {
                "amount": 0.0,
                "nameClean": "crusty bread",
                "original": "0 crusty bread",
                "unit": ""
            },
            {
                "amount": 3.0,
                "nameClean": "egg",
                "original": "3 large eggs",
                "unit": "large"
            },
            {
                "amount": 0.0,
                "nameClean": "extra virgin olive oil",
                "original": "0 extra virgin olive oil, for dipping bread, optional",
                "unit": ""
            },
            {
                "amount": 1.5,
                "nameClean": "wheat flour",
                "original": "1.5 c flour",
                "unit": "c"
            },
            {
                "amount": 2.0,
                "nameClean": "olive oil",
                "original": "2 c olive oil",
                "unit": "c"
            },
            {
                "amount": 0.0,
                "nameClean": "salt and pepper",
                "original": "0 salt and black pepper to taste",
                "unit": ""
            }
        ],
        "id": 6,
        "image": "https://img.spoonacular.com/recipes/6-556x370.jpg",
        "instructions": [
            "If you are using whole, fresh anchovies you must clean them first. Pull off the heads and pull out the insides. Then rinse with clean water.",
            "Pour the olive oil into a small deep saucepan set over heat. Use a deep fry thermometer to monitor the heat.Meanwhile, add the eggs to a small bowl and beat until well mixed.",
            "Add the flour, cayenne, salt and black pepper to a shallow bowl, use a fork to mix the ingredients together. Dip the fish one at a time into the beaten eggs and then roll it in flour.When the oil reaches 365 degrees F. fry the fish a few at a time, rolling them around in the oil to assure even cooking until they are golden brown (about 5-8 minutes).",
            "Serve with crusty bread, extra-virgin olive oil for dipping the bread (optional) and tomatoes."
        ],
        "missedIngredients": [],
        "readyInMinutes": 15,
        "servings": 15,
        "summary": "Fried Anchovies is a <b>dairy free and pescatarian</b> recipe with 15 servings. This hor d'oeuvre has <b>354 calories</b>, <b>9g of protein</b>, and <b>31g of fat</b> per serving. For <b>$1.5 per serving</b>, this recipe <b>covers 8%</b> of your daily requirements of vitamins and minerals. A mixture of salt and pepper, cayenne pepper, flour, and a handful of other ingredients are all it takes to make this recipe so delicious. 1 person were glad they tried this recipe. From preparation to the plate, this recipe takes around <b>15 minutes</b>. It is brought to you by SippitySup. Overall, this recipe earns a <b>not so great spoonacular score of 39%</b>. Similar recipes include <a href=\"https://spoonacular.com/recipes/fried-anchovies-253335\">Fried Anchovies</a>, <a href=\"https://spoonacular.com/recipes/fried-anchovies-with-sage-1189555\">Fried Anchovies with Sage</a>, and <a href=\"https://spoonacular.com/recipes/fried-anchovies-with-sage-1201577\">Fried Anchovies with Sage</a>.",
        "title": "Fried Anchovies"
    }
}   
    recipe_2 = {"recipes": {
        "extendedIngredients": [
            {
                "amount": 1.0,
                "nameClean": "pastina",
                "original": "Sale e pepe",
                "unit": "serving"
            },
            {
                "amount": 1.0,
                "nameClean": "almonds",
                "original": "A handful of almonds",
                "unit": "handful"
            },
            {
                "amount": 0.8,
                "nameClean": "boquerones",
                "original": "4/5 Anchovies (or Sardines)",
                "unit": ""
            },
            {
                "amount": 2.0,
                "nameClean": "carrot",
                "original": "2 raw pealed carrots",
                "unit": ""
            },
            {
                "amount": 1.0,
                "nameClean": "cauliflower",
                "original": "A quarter of a raw cauliflower",
                "unit": "serving"
            },
            {
                "amount": 1.0,
                "nameClean": "extra virgin olive oil",
                "original": "Extra virgin olive oil",
                "unit": "serving"
            },
            {
                "amount": 3.0,
                "nameClean": "extra virgin olive oil",
                "original": "Dressing: Extra virgin olive oil, Salt and pepper, 3 Tbs Lemon juice",
                "unit": "Tbs"
            },
            {
                "amount": 3.0,
                "nameClean": "lemon juice",
                "original": "3 Tbs Lemon juice",
                "unit": "Tbs"
            },
            {
                "amount": 50.0,
                "nameClean": "arugula",
                "original": "Rocket (arugula) 50gr",
                "unit": "gr"
            },
            {
                "amount": 1.0,
                "nameClean": "salt and pepper",
                "original": "Salt and pepper",
                "unit": "serving"
            }
        ],
        "id": 3,
        "image": "https://img.spoonacular.com/recipes/3-556x370.jpg",
        "instructions": [],
        "missedIngredients": [],
        "readyInMinutes": 45,
        "servings": 1,
        "summary": "Carrots, Cauliflower And Anchovies is a <b>dairy free and pescatarian</b> recipe with 1 servings. For <b>$2.8 per serving</b>, this recipe <b>covers 29%</b> of your daily requirements of vitamins and minerals. One portion of this dish contains about <b>17g of protein</b>, <b>73g of fat</b>, and a total of <b>947 calories</b>. 1 person were impressed by this recipe. Only a few people really liked this main course. Head to the store and pick up sale e pepe, extra virgin olive oil, anchovies, and a few other things to make it today. It is brought to you by saladpride.blogspot.com. From preparation to the plate, this recipe takes around <b>45 minutes</b>. With a spoonacular <b>score of 76%</b>, this dish is pretty good. Try <a href=\"https://spoonacular.com/recipes/grilled-peppers-with-anchovies-feta-cheese-and-spaghetti-645795\">Grilled Peppers With Anchovies, Feta Cheese and Spaghetti</a>, <a href=\"https://spoonacular.com/recipes/italian-string-beans-with-anchovies-and-breadcrumbs-648259\">Italian String Beans With Anchovies and Breadcrumbs</a>, and <a href=\"https://spoonacular.com/recipes/broccoli-rabe-with-tomatoes-anchovies-spaghetti-636212\">Broccoli Rabe with Tomatoes, Anchovies & Spaghetti</a> for similar recipes.",
        "title": "Carrots, Cauliflower And Anchovies"
    }
}
    
    import pytest

@pytest.fixture
def added_ingredient(auth_client):
    response = auth_client.post("/ingredients", json={"name": "Tomato"})
    return response.json["ingredient"]["id"]

    

    db.session.add_all([recipe_1, recipe_2])

    db.session.commit()