import pytest
import sys
sys.path.append('/home/gregory/webdev/inventory/')
from app import create_app, mongo
from app.models import InStock
from app.func_helpers import createProductDict


@pytest.fixture(scope='module')
def client():
    app = create_app()
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()
 
    #create the database and load test data
    with app.app_context():
        mongo.db.products.drop()
        mongo.db.instock.drop()
        product = dict(manufacturer='CVI', part_number='TLM1', price='1000.00',
                       description='a mirror', diameter=1, coating='DIELECTRIC', curvature=0)
        product_dict = createProductDict('OPTICS', 'MIRRORS', product)
        stock = InStock(code='CVI-TLM1', quantity=int(10), room='JA212',
                         location='cabinet A')
        mongo.db.products.insert_one(product_dict)
        mongo.db.instock.insert_one(stock.__dict__)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()
