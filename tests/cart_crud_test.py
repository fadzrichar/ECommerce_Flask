import json
from . import app, client, cache, create_token, reset_db

class TestCartCrud():
	reset_db()

	def test_post_new_cart(self, client):
		token = create_token(False)

		data = {
			"cart_status": False,
			"product_id": 1,
			"product_name": "Banpresto Onepiece Stampede Movie",
			"url_photo": "https://images-na.ssl-images-amazon.com/images/I/91VEQYGJXDL._SL1500_.jpg",
			"price": 1000000,
			"stock": 1,
			"category": "Digimon",
			"product_weight":1.0,
			"fullname": "Charisma Fadzri Triprakoso",
			"email": "fadzri@alterra.id"
		}

		res = client.post('/carts/add', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200

	def test_put_cart(self, client):
		token = create_token(False)

		data = {
				"cart_status":False,
				"stock":2
		}

		res = client.put('/carts/1', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200
	
	def test_get_id_cart(self, client):
		token = create_token(False)

		res = client.get('/carts/1', headers={'Authorization': 'Bearer ' + token})

		assert res.status_code == 200

	def test_get_all_cart(self, client):
		token = create_token(False)

		res = client.get('/carts/list', headers={'Authorization': 'Bearer ' + token})

		assert res.status_code == 200

	def test_delete_by_id_carts(self, client):
		token = create_token(False)
		res = client.delete('/carts/1', headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200

	def test_cart_valid_option_add(self, client):
		token = create_token(False)
		res = client.options('/carts/add', headers={'Authorization': 'Bearer ' + token})

		res_json = json.loads(res.data)
		assert res.status_code == 200

	def test_cart_valid_option_list(self, client):
		token = create_token(False)
		res = client.options('/carts/list', headers={'Authorization': 'Bearer ' + token})

		res_json = json.loads(res.data)
		assert res.status_code == 200

	def test_cart_valid_option_resource(self, client):
		token = create_token(False)
		res = client.options('/carts/1', headers={'Authorization': 'Bearer ' + token})

		res_json = json.loads(res.data)
		assert res.status_code == 200