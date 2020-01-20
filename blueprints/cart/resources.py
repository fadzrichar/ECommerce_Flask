from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from flask_jwt_extended import jwt_required, get_jwt_claims
from datetime import datetime
from sqlalchemy import desc
from .model import Carts
from blueprints.user.model import Users
from blueprints.product.model import Products
from blueprints.transaction.model import TransactionDetails
from blueprints import db, app
from datetime import datetime
import json, hashlib
from blueprints import internal_required

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class cartResource(Resource):  
    def options(self, id=None):
        return {"status":"ok"},200

    @jwt_required
    def delete(self,id):
        qry = Carts.query.get(id)

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


    # add to carts
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, location="json")
        parser.add_argument("quantity", type=int, location="json")
        args = parser.parse_args()

        claims = get_jwt_claims()
        user_id = claims['id']
        # print('claims', claims['id'])
        # print('user', user_id)

        product = Products.query.get(args["product_id"])
        if product is None:
            return {"message":"Products Not Available"}, 404
        cart = Carts.query.filter_by(status=True)
        cart = cart.filter_by(user_id=user_id).first()
        if cart == None:
            cart = Carts(user_id)
            db.session.add(cart)
            db.session.commit()
        print('cart', cart)
        transaction = TransactionDetails(args["product_id"], cart.id, product.price, args["quantity"])
        db.session.add(transaction)
        db.session.commit()

        cart.total_item += args["quantity"]
        cart.total_item_price += (int(product.price)*int(args["quantity"]))
        cart.updated_at = datetime.now()
        db.session.commit()
        # return {"status":"Carts added"}, 200
        return marshal(cart, Carts.response_fields), 200

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        cart = Carts.query.filter_by(user_id=claims["id"])
        cart = cart.filter_by(status=True)
        cart = cart.all()
        result=[]
        for qry in cart:
            marshalqry = marshal(qry, Carts.response_fields)
            transaction = TransactionDetails.query.filter_by(cart_id=qry.id)
            transaction = transaction.all()
            list_transaction = []
            for td in transaction:
                product = Products.query.filter_by(id=td.product_id).first()
                marshalProduct = marshal(product, Products.response_fields)
                marshaltd = marshal(td, TransactionDetails.response_fields)
                marshaltd["product_id"] = marshalProduct
                list_transaction.append(marshaltd)
            result.append({"cart":marshalqry,"transaction_detail": list_transaction})
        return result, 200

    @jwt_required
    @internal_required
    def patch(self):
        return 'Not yet implement', 501

    
api.add_resource(cartResource, '','/<int:id>')