import requests
import pytest
import jwt
import datetime
from rest import app
from logger.logs import logger


req_id = None
token = jwt.encode({'id': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                   app.config['SECRET_KEY'], algorithm='HS256')
URL = ''
client = app.test_client()


def test_post():
    try:
        response = client.post(f'{URL}/req', json={'token': token,
                                                     'sender': 5,
                                                     'change_department_id': 1,
                                                     'increase_salary': 20})
        global req_id
        #req_id = response.json['id']
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get():
    try:
        response = client.get(f'{URL}/req/{req_id}', json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_patch():
    try:
        response = client.patch(f'{URL}/req/{req_id}', json={'token': token,
                                                               'status': 2})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get_fail():
    try:
        response = client.get(f'{URL}/req/0', json={'token': token})
        assert response.status_code == 404
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get_requests():
    try:
        response = client.get(f'{URL}/reqs', json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Sign in test failed ({type(e).__name__}:{e})')
        print(f'Sign in test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Sign in test failed ({type(e).__name__}:{e})')
