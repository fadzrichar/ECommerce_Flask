from blueprints import db
from flask_restful import fields
import datetime

class Products(db.Model):
	__tablename__= "product"
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	product_name = db.Column(db.String(255), nullable=False)
	stock = db.Column(db.Integer, nullable=False)
	price = db.Column(db.Integer, nullable=False)
	category = db.Column(db.String(25), nullable=False)
	url_photo1 = db.Column(db.String(1000))
	url_photo2 = db.Column(db.String(1000))
	url_photo3 = db.Column(db.String(1000))
	url_photo4 = db.Column(db.String(1000))
	weight = db.Column(db.Integer, default=1)
	description = db.Column(db.String(255), nullable=False)  
	created_at = db.Column(db.DateTime, default = datetime.datetime.now())
	updated_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())  

	response_fields = {
		'id' : fields.Integer,
		'product_name' : fields.String,
		'stock' : fields.Integer,
		'price' : fields.Integer,
		'category' : fields.String,
		'url_photo1' : fields.String,
		'url_photo2' : fields.String,
		'url_photo3' : fields.String,
		'url_photo4' : fields.String,
		'weight' : fields.Integer,
		'description' : fields.String,
		'created_at' : fields.DateTime,
		'updated_at' : fields.DateTime
	}

	def __init__(self, product_name, stock, price, category, url_photo1, url_photo2, url_photo3, url_photo4, weight, description):
		self.product_name = product_name
		self.stock = stock
		self.price = price
		self.category = category
		self.url_photo1 = url_photo1
		self.url_photo2 = url_photo2
		self.url_photo3 = url_photo3
		self.url_photo4 = url_photo4
		self.weight = weight
		self.description = description

	def __repr__(self):
		return '<Product %r>' % self.id