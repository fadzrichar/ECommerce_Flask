import pytest, json, logging
from flask import Flask, request
from blueprints import app, db
from blueprints.cart.model import Carts
from blueprints.product.model import Products
from blueprints.transaction.model import Transactions
from blueprints.user.model import Users
from app import cache, app

# Password Encription
from password_strength import PasswordPolicy
import hashlib

def reset_db():
    db.drop_all()
    db.create_all()

    password_1 = hashlib.md5("charisma".encode()).hexdigest()
    user1 = Users('fadzri', 'fadzricharisma@gmail.com', password_1,'laki-laki','13 Maret 1993','085746363633')
    db.session.add(user1)
    db.session.commit()

    password_2 = hashlib.md5("wahyuni".encode()).hexdigest()
    user2 = Users('dwi', 'dwiwahyuni@gmail.com', password_2,'perempuan','31 Maret 1994','085749600262')
    db.session.add(user2)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client
    
@pytest.fixture
def client(request):
    return call_client(request)

def create_token(isInternal=False):
    if isInternal:
        cachename = 'test-admin-token'
        data = {
            "username":"admin",
            "password":"adminfadzri"
        }
    else:
        cachename = 'test-nonadmin-token'
        data = {
            'username':'fadzri',
            'password':'charisma'
        }
    token = cache.get(cachename)
    # prepare request input
    
    if token is None:
        # do request
        req = call_client(request)
        res = req.get('/login',
                        query_string=data)

        # store respons
        res_json = json.loads(res.data)

        logging.warning('RESULT: %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 200

        # save token into cache
        cache.set(cachename, res_json['token'], timeout=60)

        # return, bcz it usefull for other test
        return res_json['token']
    else:
        return token