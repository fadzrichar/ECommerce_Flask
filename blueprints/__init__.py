import json, os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from datetime import timedelta
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_cors import CORS

app = Flask(__name__)
app.config['APP_DEBUG'] = True
CORS(app)

uname = os.environ["THIS_UNAME"]
pwd = os.environ["THIS_PWD"]
# db_test = os.environ["THIS_DB_TEST"]
db_dev = os.environ["THIS_DB_DEV"]
db_endpoint = os.environ["THIS_DB_ENDPOINT"]

try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{uname}:{pwd}@0.0.0.0:3306/ECommerce_test".format(uname=uname, pwd=pwd)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{uname}:{pwd}@{db_endpoint}:3306/{db_dev}".format(uname=uname, pwd=pwd, db_dev=db_dev, db_endpoint=db_endpoint)
		# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta1234@ecommerce.czyclfjzsfbe.ap-southeast-1.rds.amazonaws.com:3306/ecommerce'
except Exception as e:
    raise e

# sqlalchemy config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#######
# JWT #
#######

app.config['JWT_SECRET_KEY'] = 'FaDzRiChArIsMa'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# jwt custom decorator admin


def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['username'] != 'admin':
            return {'status': 'FORBIDDEN', 'message': 'Admin Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

##############################
# SQLAlchemy Database config #
##############################


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    # if request.method == 'GET':
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s",
                        json.dumps({
                            'status_code': response.status_code,
                            'method': request.method,
                            'code': response.status,
                            'uri': request.full_path,
                            'request': request.args.to_dict(),
                            'response': json.loads(response.data.decode('utf8'))
                        })
                        )
    elif response.status_code == 404:
        app.logger.warning("REQUEST_LOG\t%s",
                           json.dumps({
                               'status_code': response.status_code,
                               'method': request.method,
                               'code': response.status,
                               'uri': request.full_path,
                               'request': request.args.to_dict(),
                               'response': json.loads(response.data.decode('utf8'))
                           })
                           )
    else:
        app.logger.error("REQUEST_LOG\t%s",
                         json.dumps({
                             'status_code': response.status_code,
                             'method': request.method,
                             'code': response.status,
                             'uri': request.full_path,
                             'request': request.args.to_dict(),
                             'response': json.loads(response.data.decode('utf8'))
                         })
                         )

    return response


#####################
# IMPORT BLUEPRINTS #
#####################

from blueprints.transaction.resources import bp_transaction
from blueprints.cart.resources import bp_cart
from blueprints.product.resources import bp_product
from blueprints.user.resources import bp_user
from blueprints.auth import bp_auth
app.register_blueprint(bp_auth, url_prefix='/login')
app.register_blueprint(bp_user, url_prefix='/users')
app.register_blueprint(bp_product, url_prefix='/products')
app.register_blueprint(bp_cart, url_prefix='/carts')
app.register_blueprint(bp_transaction, url_prefix="/transactions")

db.create_all()
