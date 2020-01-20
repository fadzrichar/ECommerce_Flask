from blueprints import db
from flask_restful import fields
from datetime import datetime

class Destinations(db.Model):
    __tablename__ = "destination"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    city_type = db.Column(db.String(255), default='')
    city_name = db.Column(db.String(255), default='')
    status = db.Column(db.Boolean, default=True)
    courier = db.Column(db.String(255), default='jne')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    response_fields = {
        "id": fields.Integer,
        "cart_id": fields.String,
        "city_type": fields.String,
        "city_name": fields.String,
        "status": fields.Boolean,
        "courier": fields.String,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime
    }

    def __init__(self, cart_id)  :
        self.cart_id = cart_id
        
    def __repr__(self):
        return "<Destinations %r>" % self.id