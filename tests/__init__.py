import pytest, json, logging
from flask import Flask, request
from blueprints import app, db
from blueprints.cart.model import Carts
from blueprints.product.model import Products
from blueprints.transaction.model import TransactionDetails
from blueprints.user.model import Users
from app import cache, app

# Password Encription
from password_strength import PasswordPolicy
import hashlib

def reset_db():
    db.drop_all()
    db.create_all()

    password_1 = hashlib.md5("charisma".encode()).hexdigest()
    user1 = Users('fadzri', 'Charisma Fadzri Triprakoso', 'fadzricharisma@gmail.com', password_1,'jember','085746363633', 'https://avatars3.githubusercontent.com/u/57993771?s=400&v=4')
    db.session.add(user1)
    db.session.commit()

    password_2 = hashlib.md5("wahyuni".encode()).hexdigest()
    user2 = Users('dwiwahyuni', 'Dwi Umi Wahyuni', 'dwiwahyuni@gmail.com', password_2,'Tulungagung','085749600262','https://pbs.twimg.com/profile_images/959677400928862208/4wfFlFCI.jpg')
    db.session.add(user2)
    db.session.commit()

    product1 = Products("Banpresto Onepiece Stampede Movie", 3, 1000000, "Onepiece", "https://images-na.ssl-images-amazon.com/images/I/511GxF-3htL._SL1000_.jpg", "https://images-na.ssl-images-amazon.com/images/I/51z0wD77tGL._SL1000_.jpg", "https://images-na.ssl-images-amazon.com/images/I/51DdOvafhGL._SL1000_.jpg", "https://images-na.ssl-images-amazon.com/images/I/61Y%2BMTEJbNL._SL1000_.jpg", 1000, "Based on the One Piece: Stampede movie, Monkey D. Luffy joins the DXF series! This figure stands about 6 inches tall and is made of PVC and ABS.")
    db.session.add(product1)
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
            "username": "admin",
            "password": "adminfadzri"
        }
    else:
        cachename = 'test-nonadmin-token'
        data = {
            "username": "fadzri",
            "password": "charisma"
        }
    token = cache.get(cachename)
    # prepare request input
    
    if token is None:
        # do request
        req = call_client(request)
        res = req.post('/login', json=data)

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