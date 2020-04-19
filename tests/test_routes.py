from app import mongo, bcrypt

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_user(client):
    user = mongo.db.user.find_one({'username':'username'})
    assert user is not None
    assert bcrypt.check_password_hash(user['password'], 'password')==True

def test_valid_login_logout(client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = client.post('/',
                            data=dict(username='username', 
                                      password='password'),
                            follow_redirects=True)
    assert response.status_code == 200
    
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Username" in response.data


def test_access_unauthorised(client):
    """
        GIVEN a Flask application
        WHEN the user in not logged in
        THEN check the response is unauthorised (401)
    """
    response = client.get('/main')
    assert response.status_code == 401

    response = client.get('/item/new')
    assert response.status_code == 401

    response = client.get('/item/new/Optics/MIRRORS')
    assert response.status_code == 401

    response = client.get('/item/view/CVI-TLM1')
    assert response.status_code == 401

    response = client.get('/item/update/CVI-TLM1')
    assert response.status_code == 401

    response = client.get('/item/store/CVI-TLM1')
    assert response.status_code == 401   

    response = client.get('/inventory/search')
    assert response.status_code == 401

    response = client.get('/inventory/{"type":"MIRRORS"}')
    assert response.status_code == 401

    response = client.get('/item/delete/CVI-TLM1')
    assert response.status_code == 401

    response = client.get('/locations')
    assert response.status_code == 401  


def test_access_authorised(client):
    """
        GIVEN a Flask application
        WHEN the user is logged in
        THEN check the response is authorised (200)
    """
    client.post('/', data=dict(username='username', password='password'),
                follow_redirects=True)

    response = client.get('/main')
    assert response.status_code == 200

    response = client.get('/item/new')
    assert response.status_code == 200

    response = client.get('/item/new/Optics/MIRRORS')
    assert response.status_code == 200

    response = client.get('/item/view/CVI-TLM1')
    assert response.status_code == 200

    response = client.get('/item/update/CVI-TLM1')
    assert response.status_code == 200

    response = client.get('/item/store/CVI-TLM1')
    assert response.status_code == 200   

    response = client.get('/inventory/search')
    assert response.status_code == 200

    response = client.get('/inventory/{"type":"MIRRORS"}')
    assert response.status_code == 200

    response = client.get('/item/delete/CVI-TLM1')
    assert response.status_code == 200

    response = client.get('/locations')
    assert response.status_code == 200 


# def test_newItem_post_success(client):
#     product = dict(type='MIRRORS', manufacturer='CVI', part_number='TLM2', dimension_unit='MM',
#                    diameter=1, price='1000.00', currency='EUR', description='a mirror')
#     response = client.post('/item/new', data=product, follow_redirects=True)
#     assert response.status_code == 401


# def test_newItem_post_inDatabase(client):
#     product = dict(manufacturer='CVI', part_number='TLM1',
#                    group='optics', description='a mirror')
#     response = client.post('/item/new', data=product, follow_redirects=True)    
#     assert b'database' in response.data
#     assert response.status_code == 200






 