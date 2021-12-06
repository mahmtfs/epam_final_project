import requests
import pytest
import jwt
import datetime
from app import app
from logger.logs import logger
from config import URL


req_id = None
token = jwt.encode({'id': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                   app.config['SECRET_KEY'], algorithm='HS256')


def test_post():
    try:
        response = requests.post(f'{URL}/req', json={'token': token,
                                                     'sender': 2,
                                                     'change_department_id': 1,
                                                     'increase_salary': 20})
        global req_id
        req_id = response.json()['id']
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get():
    try:
        response = requests.get(f'{URL}/req/{req_id}', json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_patch():
    try:
        response = requests.patch(f'{URL}/req/{req_id}', json={'token': token,
                                                               'status': 2})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get_fail():
    try:
        response = requests.get(f'{URL}/req/0', json={'token': token})
        assert response.status_code == 404
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get_requests():
    try:
        response = requests.get(f'{URL}/reqs', json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Sign in test failed ({type(e).__name__}:{e})')
        print(f'Sign in test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Sign in test failed ({type(e).__name__}:{e})')
