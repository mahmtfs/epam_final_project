from flask import request, url_for
import requests
import requests_mock


token = None


def test_register():
    response = requests.post(url_for('register'),
                             json={'firstname': 'test',
                                   'lastname': 'test',
                                   'email': 'test@gmail.com',
                                   'password': 'test',
                                   'birth_date': '1999-11-11',
                                   'dep_title': 'Design'})
    assert response.status_code == 201


def test_login():
    response = requests.post(url_for('login'), json={'email': 'test@gmail.com',
                                                                      'password': 'test'})
    if 'token' in response.json():
        global token
        token = response.json()['token']
    assert 'token' in response.json() is True

def test_get_employees():
    response = requests.get(url_for('get_all_employees'),
                            json={'token': token})
    assert response.status_code == 200
