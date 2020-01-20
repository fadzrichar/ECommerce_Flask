from blueprints import db
from flask_restful import fields
from blueprints.user.model import Users
from blueprints.product.model import Products
from datetime import datetime

class Carts(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_item = db.Column(db.Integer, default=0)
    total_item_price = db.Column(db.Integer, default=0)
    total_price = db.Column(db.Integer, default=0)
    total_weight = db.Column(db.Integer, default=0)
    shipping_cost = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    response_fields = {
        'id': fields.Integer,
        'user_id' : fields.Integer,
        'total_item' : fields.Integer,
        "total_item_price": fields.Integer,
        "total_price": fields.Integer,
        'total_weight' : fields.Float,
        'shipping_cost' : fields.Integer,
        'status' : fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<Cart %r>' % self.id