from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from datetime import datetime
from sqlalchemy import desc
from blueprints import db, app
from blueprints.transaction.model import TransactionDetails
from blueprints.cart.model import Carts
from blueprints.product.model import Products
from blueprints.destination.model import Destinations
from blueprints import internal_required
import json, requests
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)

class TransactionResources(Resource):
    def options(self, id=None):
        return {'status':'ok'}, 200

    @jwt_required
    def post(self, id=None):
        apikey = '9d62c8df51fabb19bdf00a7d1de5ee1a'
        host = 'https://api.rajaongkir.com/starter'

        cart = Carts.query.get(id)
        if cart is None:
            return {"Cart not found!"}, 404
        # print('ini cart', cart)
        claims = get_jwt_claims()
        if cart.user_id != claims["id"]:
            return {"Cart not found!"}, 404
        
        destination = Destinations.query.filter_by(cart_id = id).first()
        if destination is None:
            destination = Destinations(id)
            db.session.add(destination)
            db.session.commit()

        parser = reqparse.RequestParser()
        parser.add_argument("courier", location="json", required=True)
        parser.add_argument("city_type", location="json", default=destination.city_type)
        parser.add_argument("city_name", location="json", default=destination.city_name)
        args = parser.parse_args()

        destination.city_type = args["city_type"]
        destination.city_name = args["city_name"]
        destination.courier = args["courier"]
        destination.updated_at = datetime.now()
        db.session.commit()

        #destination city
        req = requests.get(host + '/city', params={'key':apikey})
        list_city = req.json()
        # print("list", list_city)
        list_city = list_city["rajaongkir"]["results"]
        origin = 256
        for city in list_city:
            if (city["type"].lower() == (args["city_type"]).lower()) and (city["city_name"].lower() == (args["city_name"]).lower()):
                destination = city["city_id"]
        
        # total weight
        transaction = TransactionDetails.query
        transaction = transaction.filter_by(cart_id=id).all()
        total_weight = 0
        for trans in transaction:
            product = Products.query.get(trans.product_id)
            total_weight += product.weight
        cart.total_weight = total_weight
        db.session.commit()

        #shipping cost
        req = requests.post(host + '/cost', headers={'key':apikey}, json={'origin':origin, 'destination':destination, "weight":cart.total_weight, "courier":args["courier"]})
        print('ini req', req.json())
        shipcost = req.json()
        shipcost = shipcost["rajaongkir"]["results"][0]["costs"]
        if shipcost is None:
            cart.shipping_cost = None
            db.session.commit()
            return {"message":"service not available for your request"}, 400
        cart.shipping_cost = shipcost[0]["cost"][0]["value"]
        cart.total_price = cart.total_item_price + cart.shipping_cost
        db.session.commit()

        return marshal(cart, Carts.response_fields), 200

    @jwt_required
    def get(self, id=None):
        claims = get_jwt_claims()
        cart = Carts.query.filter_by(user_id=claims["id"])
        cart = cart.filter_by(id=id).first()

        if cart is None:
            return {"Cart not found!"}, 404
        if cart.total_price == 0:
            cart.total_price = cart.total_item_price
        trans = TransactionDetails.query.filter_by(cart_id=cart.id)
        trans = trans.all()
        marshalCart = marshal(cart, Carts.response_fields)
        marshaltrans = marshal(trans, TransactionDetails.response_fields)
        return [{"cart":marshalCart, "transaction detail":marshaltrans}], 200

    @jwt_required
    def delete(self,id):
        qry = TransactionDetails.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        # Hard Delete
        db.session.delete(qry)
        db.session.commit()

        # Soft Delete
        # qry.status = False,
        # print('liat qry', qry)
        # db.session.commit()
        return {'status':'Deleted'}, 200

api.add_resource(TransactionResources, "", "/<int:id>")