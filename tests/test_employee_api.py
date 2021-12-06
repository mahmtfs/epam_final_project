import requests
import pytest
from logger.logs import logger
from config import URL


token = None
emp_id = None


def test_register():
    try:
        response = requests.post(f'{URL}/api_register',
                                 json={'firstname': 'test',
                                       'lastname': 'test',
                                       'email': 'test@gmail.com',
                                       'password': 'test',
                                       'birth_date': '1999-11-11',
                                       'dep_title': 'Planning'})
        assert response.status_code == 201
    except Exception as e:
        logger.error(f'Register test failed ({type(e).__name__}:{e})')
        print(f'Register test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Register test failed ({type(e).__name__}:{e})')
    
    
def test_login():
    try:
        response = requests.post(f'{URL}/api_login', json={'email': 'test@gmail.com',
                                                           'password': 'test'})
        if 'token' in response.json():
            global token
            global emp_id
            emp_id = response.json()['current_user_id']
            token = response.json()['token']
        assert 'token' in response.json()
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_patch():
    try:
        response = requests.patch(f'{URL}/emp/{emp_id}', json={'token': token,
                                                               'password': 'test2'})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_login_fail():
    try:
        response = requests.post(f'{URL}/api_login', json={'email': 'test@gmail.com',
                                                           'password': 'test'})
        assert response.status_code == 401
    except Exception as e:
        logger.error(f'Login test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Login test failed ({type(e).__name__}:{e})')


def test_delete():
    try:
        response = requests.delete(f'{URL}/emp/{emp_id}', json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Delete test failed ({type(e).__name__}:{e})')
        print(f'Login test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Delete test failed ({type(e).__name__}:{e})')


def test_get_employees():
    try:
        response = requests.get(f'{URL}/emps',
                                json={'token': token})
        assert response.status_code == 200
    except Exception as e:
        logger.error(f'Sign in test failed ({type(e).__name__}:{e})')
        print(f'Sign in test failed ({type(e).__name__}:{e})')
        pytest.fail(f'Sign in test failed ({type(e).__name__}:{e})')
