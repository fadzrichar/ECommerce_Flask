import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from sqlalchemy import desc
from .model import Products
from blueprints.cart.model import Carts
from blueprints import db, app
from flask_jwt_extended import jwt_required
from blueprints import internal_required

bp_product = Blueprint('product', __name__)
api = Api(bp_product)

class ProductResource(Resource):
	def __init__(self):
		pass
	
	def options(self, id):
		return {'status': 'Ok'}, 200
	
	# get products data by their specific id 
	def get(self, id):
		qry = Products.query.get(id)
		if qry is not None:
			return marshal(qry, Products.response_fields), 200
		return {'status': 'NOT FOUND', 'message': 'Products not found'}, 404

	# updated the products information by admin
	@jwt_required
	@internal_required
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('product_name', location='json')
		parser.add_argument('stock', type=int, location='json')
		parser.add_argument('price', type=int, location='json')
		parser.add_argument('category', location='json')
		parser.add_argument('url_photo1', location='json')
		parser.add_argument('url_photo2', location='json')
		parser.add_argument('url_photo3', location='json')
		parser.add_argument('url_photo4', location='json')
		parser.add_argument('weight', location='json')
		parser.add_argument('description', location='json')
		
		qry = Products.query.get(id)
		
		if qry is None:
			return {'status': "NOT_FOUND"}, 404

		body = parser.parse_args()
		
		qry.product_name = body['product_name']
		qry.stock = body['stock']
		qry.price = body['price']
		qry.category = body['category']
		qry.url_photo1 = body['url_photo1']
		qry.url_photo2 = body['url_photo2']
		qry.url_photo3 = body['url_photo3']
		qry.url_photo4 = body['url_photo4']
		qry.weight = body['weight']
		qry.description = body['description']

		db.session.commit()

		return marshal(qry, Products.response_fields), 200

	@jwt_required
	@internal_required
	def delete(self, id):
		qry = Products.query.get(id)
		if qry is None:
			return {'status': 'NOT_FOUND', 'message': 'Products not found'}, 404

		# hard delete
		db.session.delete(qry)
		db.session.commit()
		return {'status': 'DELETED'}, 200

class ProductPost(Resource):
	def __init__(self):
		pass
	
	def options(self):
		return {'status': 'Ok'}, 200

	# admin posted a new products
	@jwt_required
	@internal_required
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('product_name', location='json')
		parser.add_argument('stock', type=int, location='json')
		parser.add_argument('price', type=int, location='json')
		parser.add_argument('category', location='json')
		parser.add_argument('url_photo1', location='json')
		parser.add_argument('url_photo2', location='json')
		parser.add_argument('url_photo3', location='json')
		parser.add_argument('url_photo4', location='json')
		parser.add_argument('weight', location='json')
		parser.add_argument('description', location='json')

		args = parser.parse_args()

		product = Products(args['product_name'], args['stock'], args['price'], args['category'], args['url_photo1'], args['url_photo2'], args['url_photo3'], args['url_photo4'], args['weight'], args['description'])
		
		db.session.add(product)
		db.session.commit()

		app.logger.debug('DEBUG : %s', product)
		return marshal(product, Products.response_fields)


class ProductSearch(Resource):
	def __init__(self):
		pass

	def options(self):
		return {'status': 'ok'}, 200

	# search by keyword
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('p', type=int, location='args', default=1)
		parser.add_argument('rp', type=int, location='args', default=10)
		parser.add_argument('keyword', location='args', default='None')
		args = parser.parse_args()

		offset = (args['p'] * args['rp']) - args['rp']

		qry = Products.query

		if qry:
			search_result = qry.filter(Products.product_name.like('%' + args['keyword'] + '%') | Products.category.like('%' + args['keyword'] + '%'))  
			all_search = []
			for result in search_result:
				all_search.append(marshal(result, Products.response_fields))
			return all_search, 200
		else:
			return {'status': 'NOT FOUND'}, 404

api.add_resource(ProductSearch, '/search')
api.add_resource(ProductResource, '/list/<id>')
api.add_resource(ProductPost, '/add')