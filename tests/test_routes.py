def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_newItem(client):
    response = client.get('/item/new')
    assert response.status_code == 200

def test_newItem_post_success(client):
    product = dict(manufacturer='CVI', part_number='TLM2',
                   group='optics', description='a mirror')
    response = client.post('/item/new', data=product, follow_redirects=True)
    assert response.status_code == 200


# def test_newItem_post_inDatabase(client):
#     product = dict(manufacturer='CVI', part_number='TLM1',
#                    group='optics', description='a mirror')
#     response = client.post('/item/new', data=product, follow_redirects=True)    
#     assert b'database' in response.data
#     assert response.status_code == 200


def test_searchInventory(client):
    """
        GIVEN a Flask application
        WHEN the '/inventory/search' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get('/inventory/search')
    assert response.status_code == 200

