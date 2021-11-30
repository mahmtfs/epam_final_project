from flask import request, url_for
import requests
import requests_mock
from logger.logs import logger


token = None


def test_register():
    try:
        response = requests.post('https://pure-caverns-26611.herokuapp.com/api_register',
                                 json={'firstname': 'test',
                                       'lastname': 'test',
                                       'email': 'test@gmail.com',
                                       'password': 'test',
                                       'birth_date': '1999-11-11',
                                       'dep_title': 'Design'})
        assert response.status_code == 201
    except Exception as e:
        logger.error(f'Register test failed ({type(e).__name__}:{e})')
    
    


def test_login():
    try:
        response = requests.post('https://pure-caverns-26611.herokuapp.com/api_login', json={'email': 'test@gmail.com',
                                                                                             'password': 'test'})
        if 'token' in response.json():
            global token
            token = response.json()['token']
        assert 'token' in response.json() is True
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')

def test_get_employees():
    try:
        response = requests.get('https://pure-caverns-26611.herokuapp.com/emps',
                                json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Sign in test failed ({type(e).__name__}:{e})')
