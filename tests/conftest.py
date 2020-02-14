import pytest
import sys
sys.path.append('/home/gregory/webdev/inventory/')
from app import create_app, mongo
import gridfs
from app.models import InStock
from app.func_helpers import createProductDict


@pytest.fixture(scope='module')
def client():
    app = create_app()
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()
    fs=gridfs.GridFS(mongo.db)

    #create the database and load test data
    with app.app_context():
        mongo.db.products.drop()
        mongo.db.instock.drop()
        product = dict(type='MIRRORS', manufacturer='CVI', part_number='TLM1',
                       price='1000.00', description='a mirror', diameter=1,
                       coating='DIELECTRIC', curvature=0, documentation=['CVI-TLM1doctlm1.pdf'])
        product['_id'] = product['manufacturer']+'-'+product['part_number']
        stock = InStock(code='CVI-TLM1', quantity=int(10), room='JA212',
                         location='cabinet A')
        mongo.db.products.insert_one(product)
        #filename = '/home/gregory/webdev/inventory/tests/CVI-TLM1doctlm1.pdf'
        #with open(filename, 'rb') as f:
        #    fs.put(f.read(), filename='CVI-TLM1doctlm1.pdf')
        mongo.db.instock.insert_one(stock.__dict__)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()
