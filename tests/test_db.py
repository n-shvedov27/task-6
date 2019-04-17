from http import HTTPStatus
from flask import url_for


def test_currency_creating(app, testing_db):
    with app.test_client() as client:
        headers = {
            'Content-Type': 'multipart/form-data;',
        }
        data = {
            'currency_name': 'gold',
            'cost': 2
        }
        url = '/create_currency'
        response = client.post(url, data=data, headers=headers)

        currencies = testing_db.execute("SELECT * FROM currency")

        assert str(list(currencies)[0]).endswith("'gold', 2.0)")
        assert response.status_code == HTTPStatus.OK


def test_registration(app, testing_db):
    with app.test_client() as client:
        headers = {
            'Content-Type': 'multipart/form-data;',
        }
        data = {
            'client_name': 'nik',
            'password': 'qwerty'
        }
        url = '/register'

        response = client.post(url, data=data, headers=headers)

        currencies = testing_db.execute("SELECT * FROM client")

        assert 'nik' in str(list(currencies)[0])
        assert response.status_code == HTTPStatus.FOUND


def test_routing(client):
    pass
