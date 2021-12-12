import requests
import pytest
import jwt
import datetime
from app import app
from logger.logs import logger
from config import URL


dep_id = None
token = jwt.encode({'id': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                   app.config['SECRET_KEY'], algorithm='HS256')


def test_post():
    try:
        response = requests.post(f'{URL}/dep', json={'token': token,
                                                     'title': 'test',
                                                     'salary': 300.0})
        assert response.status_code == 201
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get():
    try:
        response = requests.get(f'{URL}/dep/test', json={'token': token})
        global dep_id
        dep_id = response.json()['department']['id']
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_patch():
    try:
        response = requests.patch(f'{URL}/dep/{dep_id}', json={'token': token,
                                                               'title': 'test2'})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_get_fail():
    try:
        response = requests.get(f'{URL}/dep/0', json={'token': token})
        assert response.status_code == 404
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_delete():
    try:
        response = requests.delete(f'{URL}/dep/{dep_id}', json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Delete test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Delete test failed ({type(e).__name__}:{e})')


def test_get_departments():
    try:
        response = requests.get(f'{URL}/deps',
                                json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Sign in test failed ({type(e).__name__}:{e})')
        print(f'Sign in test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Sign in test failed ({type(e).__name__}:{e})')