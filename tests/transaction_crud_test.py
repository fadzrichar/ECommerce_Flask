import json
from . import app, client, cache, create_token, reset_db

class TestTransactionsCrud():
	idtransaction = 0
	# Test Case Create Token 
	reset_db()
	def test_post_transaction(self, client):
		token = create_token(True)

		data = {
            	"cart_id":1,
                "address":"Perumahan Tegal Besar Permai",
                "subdistrict":"kaliwates",
                "city":"Jember",
                "province":"East Java",
                "zipcode":"69132",
                "phone":"085746363633"
        }

		res = client.post('/transactions/courier', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200