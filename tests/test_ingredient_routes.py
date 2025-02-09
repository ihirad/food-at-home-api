

def test_all_ingredients_with_no_ingredients(client, test_user, clear_db):
    response = client.post("/users/login", json={"username": "marjana", "password": "abcd"})
    assert response.status_code == 200

    response = client.get("/ingredients")
    assert response.status_code == 200
    assert response.json == {"ingredients": []}  

