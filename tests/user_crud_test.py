import json, sys
from . import app, client, cache, create_token, reset_db

sys.path.append('path')

class TestUsersCrud():
    iduser = 0
    reset_db()

    def test_user_valid_input_post_name(self, client):
        data = {
                "username": "arline",
                "fullname": "Charisma Aoraline Hafidha",
                "email": "arlinehafidha@gmail.com",
                "password": "aoraline",
                "address": "Jember",
                "phone": "085100329537",
                "image": "https://pbs.twimg.com/profile_images/959677400928862208/4wfFlFCI.jpg"
        }
        
        res = client.post('/users/registration',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        TestUsersCrud.iduser = res_json['id']
        assert res.status_code == 200

    def test_user_getlist(self, client):
        token = create_token(True)

        data = {

        }

        res = client.get('/users/list', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_invalid_user_getlist(self, client):
        token = create_token()
        res = client.get('/users/list1', 
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/users/me',
                         headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_get_invalid_id_token(self, client):
        res = client.get('/users/me',
                         headers={'Authorization': 'Bearer '})

        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_user_valid_put_token(self, client):
        token = create_token()
        data = {
                "username": "fadzri",
                "phone": "085746363633"
        }
        res = client.put('/users/me/' + str(TestUsersCrud.iduser), json=data,
                         headers={'Authorization': 'Bearer ' + token},content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_invalid_put_token(self, client):
        token = create_token()
        data = {
                "username": "arline",
                "email": "arlinehafidha@gmail.com",
                "phone": "1234567890"
        }
        res = client.put('/users/me/15',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_valid_option(self, client):
        res = client.options('/users/me')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_valid_option_resource(self, client):
        res = client.options('/users/me')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_valid_option_token(self, client):
        res = client.options('/users/registration')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_valid_delete_token(self, client):
        token = create_token(True)
        res = client.delete('/users/me/' + str(TestUsersCrud.iduser),
                            headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/users/me/12',
                            headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 403