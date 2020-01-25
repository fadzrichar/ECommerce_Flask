import json, hashlib, logging
from . import client, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims

class TestCheckoutCRUD():
    reset_db()
    # GET Data for checkout page
    def test_transaction_get(self, client):
        token = create_token()
        data = {}
        res = client.get("/transactions/1", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    def test_transaction_post(self, client):
        token = create_token()
        data = {
			"courier": "jne", 
			"city_type": "Kabupaten",
			"city_name": "Jember"
			}
        res = client.post("/transactions/1", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200