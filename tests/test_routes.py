def test_home_page(client):
    """
        GIVEN a Flask application
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get('localhost/')
    assert response.status_code == 200