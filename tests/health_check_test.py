def test_health_check(test_client):
    response = test_client.get('profile/', content_type="application/json")
    assert response.status_code == 200
    assert response.text == '"OK"\n'
