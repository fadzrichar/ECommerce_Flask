from blueprints import db
from flask_restful import fields
import datetime

class Users(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(190), unique=True, nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(190), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255),nullable=False)
    image = db.Column(db.String(1000),nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    

    response_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'fullname' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'address' : fields.String,
        'phone' : fields.String,
        "image": fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'fullname' : fields.String,
        'email' : fields.String,
        'address' : fields.String,
        'phone' : fields.String,
        'image' : fields.String
    }

    def __init__(self, username, fullname, email, password, address, phone, image):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone
        self.image = image

    def __repr__(self):
        return '<User %r>' % self.id
