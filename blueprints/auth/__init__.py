from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from ..user.model import Users

from password_strength import PasswordPolicy
import hashlib

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
	def options(self):
		return 200

	def post(self):
		# Create Token
		parser = reqparse.RequestParser()
		parser.add_argument('username', location='json', required=True)
		parser.add_argument('password', location='json', required=True)
		args = parser.parse_args()

		# Internal Admin
		if args['username'] == 'admin' and args['password'] == 'adminfadzri':
			token = create_access_token(identity = args['username'], user_claims={'username': args['username']})
			return {'token': token}, 200

		# Non-Internal, Users
		else:
			password_digest = hashlib.md5(args['password'].encode()).hexdigest()
			qry = Users.query.filter_by(username = args['username']).filter_by(password = password_digest)
			userData = qry.first()
			if userData is not None:
				userData = marshal(userData, Users.jwt_claims_fields)
				token = create_access_token(identity = args['username'], user_claims=userData)
				return {'token': token}, 200
			return {'status': 'BAD REQUEST', 'message': 'invalid username or password'}, 400

	# Show the payload
	@jwt_required
	def get(self):
		verify_jwt_in_request()
		claims = get_jwt_claims()
		claims = marshal(claims, Users.jwt_claims_fields)
		return claims, 200
		
api.add_resource(CreateTokenResource, '')