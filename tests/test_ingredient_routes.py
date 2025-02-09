def test_all_ingredients_with_no_ingredients(client, test_user):
    response = client.post("/users/login", json={"username": "marjana", "password": "abcd"})
    assert response.status_code == 200
    
    
    
   
   
    