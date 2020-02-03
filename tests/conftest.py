import pytest
import sys
sys.path.append('/home/gregory/webdev/inventory/')
from app import create_app


@pytest.fixture(scope='module')
def client():
    print('Initialise client')
    app = create_app()
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()
 
 
# @pytest.fixture(scope='module')
# def init_database():
#     ''' clean and create documents in the collections of test database '''
#     print('initialisation database')
#     mongo.db.products.drop()
#     product = {'manufacturer':'CVI', 'part_number':'TLM1',
#                '_id':'CVI-TLM1', 'group':'OPTICS', 
#                'description':'a mirror'}
#     mongo.db.products.insert_one(product)

 
#     yield mongo.db  # this is where the testing happens!