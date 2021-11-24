import unittest
import requests
from logger.logs import BASE, logger


put_user = {'firstname': 'Lue',
            'lastname': 'Johns',
            'email': 'lue@gmail.com',
            'department_id': 4}

patch_user = {'firstname': 'Joe',
              'lastname': 'Stones',
              'email': 'joe@gmail.com',
              'department_id': 3}

get_cmp = {'id': 10,
           'firstname': 'Kyle',
           'lastname': 'Stevens',
           'email': 'kyle@gmail.com',
           'department_id': 7,
           'role_id': 3,
           'salary': 800.0}

put_cmp = {'id': 13,
           'firstname': 'Lue',
           'lastname': 'Johns',
           'email': 'lue@gmail.com',
           'department_id': 4,
           'role_id': 3,
           'salary': 0.0}

patch_cmp = {'id': 13,
             'firstname': 'Joe',
             'lastname': 'Stones',
             'email': 'joe@gmail.com',
             'department_id': 3,
             'role_id': 3,
             'salary': 0.0}

delete_cmp = patch_cmp


class TestUserRESTAPI(unittest.TestCase):
    def step_get(self):
        response = requests.get(BASE + 'user/10')
        self.assertEqual(response.json(), get_cmp)

    def step_put(self):
        response = requests.put(BASE + 'user/13', put_user)
        self.assertEqual(response.json(), put_cmp)

    def step_patch(self):
        response = requests.patch(BASE + 'user/13', patch_user)
        self.assertEqual(response.json(), patch_cmp)

    def step_delete(self):
        response = requests.delete(BASE + 'user/13')
        self.assertEqual(response.json(), delete_cmp)

    def _steps(self):
        for name in ['step_get',
                     'step_put',
                     'step_patch',
                     'step_delete']:
            if name.startswith('step'):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                logger.error(f'{name} failed ({type(e).__name__}:{e})')
                self.fail(f'Employee {name} failed, check logs/tests.log for additional information')
