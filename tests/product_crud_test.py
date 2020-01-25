import json
from . import app, client, cache, create_token, reset_db

class TestProductsCrud():
	idproduct = 0
	# Test Case Create Token 
	reset_db()
	def test_post_product(self, client):
		token = create_token(True)

		data = {
				"product_name": "Banpresto Onepiece Stampede Movie",
				"stock": 3,
				"price": 1000000,
				"category": "Onepiece",
				"url_photo1": "https://images-na.ssl-images-amazon.com/images/I/511GxF-3htL._SL1000_.jpg",
				"url_photo2": "https://images-na.ssl-images-amazon.com/images/I/51z0wD77tGL._SL1000_.jpg",
				"url_photo3": "https://images-na.ssl-images-amazon.com/images/I/51DdOvafhGL._SL1000_.jpg",
				"url_photo4": "https://images-na.ssl-images-amazon.com/images/I/61Y%2BMTEJbNL._SL1000_.jpg",
				"weight":1000,
				"description": "Based on the One Piece: Stampede movie, Monkey D. Luffy joins the DXF series! This figure stands about 6 inches tall and is made of PVC and ABS."
		}

		res = client.post('/products/add', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200

	def test_post_new_product(self, client):
		token = create_token(True)

		data = {
			"product_name": "S.H. Figurants Omegamon Action Figure",
			"stock": 2,
			"price": 1000000,
			"category": "Digimon",
			"url_photo1": "https://images-na.ssl-images-amazon.com/images/I/91VEQYGJXDL._SL1500_.jpg",
			"url_photo2": "https://images-na.ssl-images-amazon.com/images/I/911pWXbAgOL._SL1500_.jpg",
			"url_photo3": "https://images-na.ssl-images-amazon.com/images/I/918CX-Ve9tL._SL1500_.jpg",
			"url_photo4": "https://images-na.ssl-images-amazon.com/images/I/91RjaSVQNhL._SL1500_.jpg",
			"weight":2000,
			"description": "Tamashii Nations introduces a new sculpt and repaint of Omegamon (Omnimon) as he appears in Digimon Adventure: Our War Game! This set includes cape attachment pieces, the Transcendent Sword, the Supreme Cannon, and display stand."
		}

		res = client.post('/products/add', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200

	def test_put_product(self, client):
		token = create_token(True)
		data = {
			"product_name": "S.H. Figurants Omegamon Action Figure",
			"stock": 3,
			"price": 1000000,
			"category": "Digimon",
			"url_photo1": "https://images-na.ssl-images-amazon.com/images/I/91VEQYGJXDL._SL1500_.jpg",
			"url_photo2": "https://images-na.ssl-images-amazon.com/images/I/911pWXbAgOL._SL1500_.jpg",
			"url_photo3": "https://images-na.ssl-images-amazon.com/images/I/918CX-Ve9tL._SL1500_.jpg",
			"url_photo4": "https://images-na.ssl-images-amazon.com/images/I/91RjaSVQNhL._SL1500_.jpg",
			"weight": 3000,
			"description": "Tamashii Nations introduces a new sculpt and repaint of Omegamon (Omnimon) as he appears in Digimon Adventure: Our War Game! This set includes cape attachment pieces, the Transcendent Sword, the Supreme Cannon, and display stand."
		}

		res = client.put('/products/list/1', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200
	
	def test_get_by_id_product(self, client):
		token = create_token()

		data = {
		}

		res = client.get('/products/list/1', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200
	
	def test_get_search(self, client):
		token = create_token(False)

		data = {
			"keyword":"Stampede"
		}

		res = client.get('/products/search', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200
	
	def test_get_search_category(self, client):
		token = create_token(False)

		data = {
			"keyword":"Digimon"
		}

		res = client.get('/products/search', json = data, headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200

	def test_delete_by_id_product_admin(self, client):
		token = create_token(True)

		res = client.delete('/products/list/2', headers={'Authorization': 'Bearer ' + token})
		res_json = json.loads(res.data)

		assert res.status_code == 200

	def test_product_valid_option_add(self, client):
		res = client.options('/products/add')

		res_json = json.loads(res.data)
		assert res.status_code == 200
	
	def test_product_valid_option_resource(self, client):
		res = client.options('/products/list/'  + str(TestProductsCrud.idproduct))

		res_json = json.loads(res.data)
		assert res.status_code == 200

	def test_user_valid_option_search(self, client):
		res = client.options('/products/search')

		res_json = json.loads(res.data)
		assert res.status_code == 200