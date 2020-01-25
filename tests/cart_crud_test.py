import json, hashlib, logging, sys
from . import client, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims
class TestCartCrud():
    reset_db()
    # POST Cart
    def test_cart_post(self, client):
        token = create_token()
        data = {
				"product_id": 1, 
        		"quantity": 1
				}
        res = client.post("/carts", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Cart 
    def test_blog_get(self, client):
        token = create_token()
        data = {}
        res = client.get("/carts", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200