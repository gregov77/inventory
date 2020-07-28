from flask import request, url_for
from app import mongo

def test_newMirror(client, auth):
    """
    GIVEN a Flask application
    WHEN data for a new mirror are posted from NewItemEntry
    THEN check the response is valid
         check redirection to the view page
         check the mirror is in the database 
    """
    auth.login()
    product = dict(manufacturer='CVI', part_number='TLM2', price='1000.00',
                description='a mirror', diameter=1, currency='GPB',
                dimension_unit='MM', coating='dielectric')
    response = client.post(
            '/item/new/Optics/MIRRORS',
            data=product,
            follow_redirects=True
        )
    assert response.status_code == 200
    assert b'CVI-TLM2' in response.data
    assert mongo.db.products.find_one({'_id':'CVI-TLM2'}) is not None
    