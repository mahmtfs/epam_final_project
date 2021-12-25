import requests
import pytest
from rest import app
from logger.logs import logger


token = None
emp_id = None
client = app.test_client()
URL = ''


def test_register():
    "testing registration"
    try:
        response = client.post(f'{URL}/api_register',
                                 json={'firstname': 'test',
                                       'lastname': 'test',
                                       'email': 'test@gmail.com',
                                       'password': 'test',
                                       'birth_date': '1999-11-11',
                                       'dep_title': 'Design'})
        assert response.status_code == 201
    except Exception as e:
        logger.error(f'Register test failed ({type(e).__name__}:{e})')
        print(f'Register test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Register test failed ({type(e).__name__}:{e})')
    
    
def test_login():
    "testing logging in"
    try:
        response = client.post(f'{URL}/api_login', json={'email': 'test@gmail.com',
                                                           'password': 'test'})
        if 'token' in response.json:
            global token
            global emp_id
            emp_id = response.json['current_user_id']
            token = response.json['token']
        assert 'token' in response.json
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_patch():
    "testing employee updating"
    try:
        response = client.patch(f'{URL}/emp/{emp_id}', json={'token': token,
                                                               'password': 'test2'})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_login_fail():
    "testing logging in failure"
    try:
        response = client.post(f'{URL}/api_login', json={'email': 'test@gmail.com',
                                                           'password': 'test'})
        assert response.status_code == 401
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_delete():
    "testing employee deleting"
    try:
        response = client.delete(f'{URL}/emp/{emp_id}', json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Delete test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Delete test failed ({type(e).__name__}:{e})')


def test_get_employees():
    "testing employees listing"
    try:
        response = client.get(f'{URL}/emps',
                                json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Sign in test failed ({type(e).__name__}:{e})')
        print(f'Sign in test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Sign in test failed ({type(e).__name__}:{e})')
