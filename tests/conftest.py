import pytest
import sys
sys.path.append('/home/gregory/Documents/webDev/inventory/')
from app import create_app, mongo, bcrypt
import gridfs
from app.models import InStock, User
from app.func_helpers import get_productDict
from app.config import Config_test
from bson import ObjectId

@pytest.fixture
def app():
    app = create_app(Config_test)
    fs=gridfs.GridFS(mongo.db)

    #create the database and load test data
    with app.app_context():
        mongo.db.products.drop()
        mongo.db.instock.drop()
        fin = fs.find_one({'filename':'CVI-TLM1doctlm1.pdf'})
        if fin:
            fs.delete(fin._id)
        filename = '/home/gregory/Documents/webDev/inventory/tests/CVI-TLM1doctlm1.pdf'
        with open(filename, 'rb') as f:
           uid = fs.put(f.read(), filename='CVI-TLM1doctlm1.pdf')
        
        product = dict(type='MIRRORS', manufacturer='CVI', part_number='TLM1',
                       price='1000.00', description='a mirror', diameter=1, currency='GPB',
                       dimension_unit='MM', coating='DIELECTRIC', 
                       documentation={str(uid):'CVI-TLM1doctlm1.pdf'})
        product['_id'] = product['manufacturer']+'-'+product['part_number']
        stock = InStock(code='CVI-TLM1', quantity=int(10), room='JA212',
                         storage='CABINET A')
        mongo.db.products.insert_one(product)
        mongo.db.instock.insert_one(vars(stock))
    
        # Create test user
        username = 'username'
        password = 'password'
        user = User(username=username, password=bcrypt.generate_password_hash(password))
        mongo.db.user.insert_one(vars(user))

    yield app    
    
    mongo.db.user.delete_one({'username':'username'})
    

@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions():
    def __init__(self, client):
        self._client = client

    def login(self, username='username', password='password'):
        return self._client.post(
            '/',
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/logout', follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)