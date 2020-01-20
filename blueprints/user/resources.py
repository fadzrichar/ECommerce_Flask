import json, hashlib
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from sqlalchemy import desc
from .model import Users
from blueprints import db, app
from blueprints import internal_required

from password_strength import PasswordPolicy

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UsersGetResource(Resource):
	def options(self):
		return {'status': 'Ok'}, 200

	# access for users who wanna know their information that have a token to login
	@jwt_required
	def get(self):
		claims = get_jwt_claims()
		id = claims['id']
		qry = Users.query.get(id)
		if qry is not None:
			return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}
		return {'status': 'NOT FOUND', 'message': 'Users not found'}, 404

	# update data for users
	@jwt_required
	def put(self, id):
		claims = get_jwt_claims()
		id = claims['id']
		qry = Users.query.get(id)
		parser = reqparse.RequestParser()
		parser.add_argument('username', location='json', required=True)
		parser.add_argument('fullname', location='json', default=qry.fullname)
		parser.add_argument('email', location='json', default=qry.email)
		parser.add_argument('address', location='json', default=qry.address)
		parser.add_argument('phone', location='json', default=qry.phone)
		parser.add_argument('image', location='json', default=qry.image)

		qry = Users.query.get(id)
		if qry is None:
			return {'status': "NOT_FOUND"}, 404

		args = parser.parse_args()
		qry.email = args['username']
		qry.email = args['fullname']
		qry.email = args['email']
		qry.address = args['address']
		qry.phone = args['phone']
		qry.image = args['image']

		db.session.commit()

		return marshal(qry, Users.response_fields), 200

	# delete users data by admin only
	@jwt_required
	@internal_required
	def delete(self, id):
		qry = Users.query.get(id)
		if qry is None:
			return {'status': 'NOT_FOUND', 'message': 'Users not found'}, 404

		# hard delete
		db.session.delete(qry)
		db.session.commit()
		return {'status': 'DELETED'}, 200


class UsersResource(Resource):
	def options(self):
		return {'status': 'Ok'}, 200

	# register a new users
	def post(self):
		policy = PasswordPolicy.from_names(
			length = 7
		)

		parser = reqparse.RequestParser()
		parser.add_argument('username', location='json', required = True)
		parser.add_argument('fullname', location='json', required = True)
		parser.add_argument('email', location='json', required = True)
		parser.add_argument('password', location='json', required = True)
		parser.add_argument('address', location='json', required = True)
		parser.add_argument('phone', location='json', required = True)
		parser.add_argument('image', location='json', required = True)

		args = parser.parse_args()

		validation = policy.test(args['password'])

		if validation == []:
			password_digest = hashlib.md5(args['password'].encode()).hexdigest()
			# Creating object
			user = Users(args['username'], args['fullname'], args['email'], password_digest, args['address'],args['phone'], args['image'])
			db.session.add(user)
			db.session.commit()

			app.logger.debug('DEBUG : %s', user)

			return marshal(user, Users.response_fields), 200, {'Content-Type':'application/json'}

class UsersList(Resource):
	# function for admin only who wnna know list users
	@jwt_required
	@internal_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('p', type=int, location='args', default=1)
		parser.add_argument('rp', type=int, location='args', default=25)
		args = parser.parse_args()

		offset = (args['p'] * args['rp']) - args['rp']

		qry = Users.query

		rows = []
		for row in qry.limit(args['rp']).offset(offset).all():
			rows.append(marshal(row, Users.response_fields))

		return rows, 200, {'Content-Type': 'application/json'}


api.add_resource(UsersGetResource, '/me', '/me/<id>')
api.add_resource(UsersResource, '/registration')
api.add_resource(UsersList, '/list')