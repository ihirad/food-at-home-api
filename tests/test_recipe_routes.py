import pytest
from app.models.recipe import Recipe

def test_get_all_recipes_no_data(auth_client):
    # Act
    response = auth_client.get("/recipes/all")
    response_body = response.json

    # Assert
    assert response.status_code == 200
    assert "recipe" in response_body
    assert response_body == {"recipe": []}


# def test_get_recipe_by_id(auth_client):
#     # Act
#     response = auth_client.get("/recipes/6")
#     response_body = response.json

#     # Assert
#     assert response.status_code == 200
#     assert "recipes" in response.json or "message" in response.json
#     assert response_body == {
#     "recipes": {
#         "extendedIngredients": [
#             {
#                 "amount": 1.0,
#                 "nameClean": "boquerones",
#                 "original": "1 lb whole fresh, or cleaned and marinated anchovies (not the salted or tinned variety)",
#                 "unit": "lb"
#             },
#             {
#                 "amount": 0.25,
#                 "nameClean": "ground cayenne pepper",
#                 "original": "0.25 t cayenne pepper",
#                 "unit": "t"
#             },
#             {
#                 "amount": 0.0,
#                 "nameClean": "cherry tomato",
#                 "original": "0 cherry tomatoes, as needed",
#                 "unit": ""
#             },
#             {
#                 "amount": 0.0,
#                 "nameClean": "crusty bread",
#                 "original": "0 crusty bread",
#                 "unit": ""
#             },
#             {
#                 "amount": 3.0,
#                 "nameClean": "egg",
#                 "original": "3 large eggs",
#                 "unit": "large"
#             },
#             {
#                 "amount": 0.0,
#                 "nameClean": "extra virgin olive oil",
#                 "original": "0 extra virgin olive oil, for dipping bread, optional",
#                 "unit": ""
#             },
#             {
#                 "amount": 1.5,
#                 "nameClean": "wheat flour",
#                 "original": "1.5 c flour",
#                 "unit": "c"
#             },
#             {
#                 "amount": 2.0,
#                 "nameClean": "olive oil",
#                 "original": "2 c olive oil",
#                 "unit": "c"
#             },
#             {
#                 "amount": 0.0,
#                 "nameClean": "salt and pepper",
#                 "original": "0 salt and black pepper to taste",
#                 "unit": ""
#             }
#         ],
#         "id": 6,
#         "image": "https://img.spoonacular.com/recipes/6-556x370.jpg",
#         "instructions": [
#             "If you are using whole, fresh anchovies you must clean them first. Pull off the heads and pull out the insides. Then rinse with clean water.",
#             "Pour the olive oil into a small deep saucepan set over heat. Use a deep fry thermometer to monitor the heat.Meanwhile, add the eggs to a small bowl and beat until well mixed.",
#             "Add the flour, cayenne, salt and black pepper to a shallow bowl, use a fork to mix the ingredients together. Dip the fish one at a time into the beaten eggs and then roll it in flour.When the oil reaches 365 degrees F. fry the fish a few at a time, rolling them around in the oil to assure even cooking until they are golden brown (about 5-8 minutes).",
#             "Serve with crusty bread, extra-virgin olive oil for dipping the bread (optional) and tomatoes."
#         ],
#         "missedIngredients": [],
#         "readyInMinutes": 15,
#         "servings": 15,
#         "summary": "Fried Anchovies is a <b>dairy free and pescatarian</b> recipe with 15 servings. This hor d'oeuvre has <b>354 calories</b>, <b>9g of protein</b>, and <b>31g of fat</b> per serving. For <b>$1.5 per serving</b>, this recipe <b>covers 8%</b> of your daily requirements of vitamins and minerals. A mixture of salt and pepper, cayenne pepper, flour, and a handful of other ingredients are all it takes to make this recipe so delicious. 1 person were glad they tried this recipe. From preparation to the plate, this recipe takes around <b>15 minutes</b>. It is brought to you by SippitySup. Overall, this recipe earns a <b>not so great spoonacular score of 39%</b>. Similar recipes include <a href=\"https://spoonacular.com/recipes/fried-anchovies-253335\">Fried Anchovies</a>, <a href=\"https://spoonacular.com/recipes/fried-anchovies-with-sage-1189555\">Fried Anchovies with Sage</a>, and <a href=\"https://spoonacular.com/recipes/fried-anchovies-with-sage-1201577\">Fried Anchovies with Sage</a>.",
#         "title": "Fried Anchovies"
#     }
# }

def test_save_recipe(auth_client, saved_recipe_payload):
    # Act
    response = auth_client.post("/recipes", json=saved_recipe_payload)
    
    # Assert
    assert response.status_code == 201  
    response_body = response.json  
    
    assert isinstance(response_body["recipe"]["id"], int)  
    assert response_body["recipe"]["image"] == saved_recipe_payload["image"]
    assert response_body["recipe"]["name"] == saved_recipe_payload["name"]
    assert response_body["recipe"]["favorite"] == saved_recipe_payload["favorite"]
    assert response_body["recipe"]["recipe_id"] == saved_recipe_payload["recipe_id"]


def test_delete_recipe_that_does_not_exist(auth_client):
    # Act
    response = auth_client.delete("/recipes/100")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" in response.json
    assert response_body == {
    "message": "Recipe id 100 is not found"
}

# def test_delete_recipe(auth_client):  
#     # Act
#     response = auth_client.delete("/recipes")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body == {
#     "message": "Recipe 2 deleted"
# }




