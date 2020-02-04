def test_home_page(client):
    """
        GIVEN a Flask application
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200


def test_newItem(client):
    """
        GIVEN a Flask application
        WHEN the '/item/new' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get('/item/new')
    assert response.status_code == 200

def test_searchInventory(client):
    """
        GIVEN a Flask application
        WHEN the '/inventory/search' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get('/inventory/search')
    assert response.status_code == 200
