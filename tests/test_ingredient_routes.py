import pytest
from app.models.ingredient import Ingredient
from app.db import db

def test_add_or_create_ingredient(auth_client):
    # Act
    response = auth_client.post("/ingredients", json={"name": "Tomato"})
    # Assert
    assert response.status_code in [200, 201]
    assert "message" in response.json
    assert "ingredient" in response.json

def test_get_all_ingredients(auth_client):
    # Act
    response = auth_client.get("/ingredients")
    # Assert
    assert response.status_code == 200
    assert "ingredients" in response.json
    assert isinstance(response.json["ingredients"], list)

def test_delete_ingredient(auth_client):
    add_response = auth_client.post("/ingredients", json={"name": "Tomato"})
    ingredient_id = add_response.json["ingredient"]["id"]
    
    # Act
    delete_response = auth_client.delete(f"/ingredients/{ingredient_id}")
    get_response = auth_client.get("/ingredients")

    # Assert
    assert delete_response.status_code == 200
    assert "message" in delete_response.json
    assert ingredient_id not in [item["id"] for item in get_response.json["ingredients"]]

