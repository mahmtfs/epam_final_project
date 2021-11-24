import unittest
import requests
from logger.logs import BASE, logger


put_request = {'sender': 5,
               'change_department_id': 6,
               'increase_salary': 5,
               'status': 0}

patch_request = {'sender': 5,
                 'change_department_id': 7,
                 'increase_salary': 2,
                 'status': 0}

get_cmp = {'id': 20,
           'sender': 6,
           'change_department_id': 6,
           'increase_salary': 0,
           'status': 2}

put_cmp = {'id': 29,
           'sender': 5,
           'change_department_id': 6,
           'increase_salary': 5,
           'status': 0}

patch_cmp = {'id': 29,
             'sender': 5,
             'change_department_id': 7,
             'increase_salary': 2,
             'status': 0}

delete_cmp = patch_cmp


class TestRequestRESTAPI(unittest.TestCase):
    def step_get(self):
        response = requests.get(BASE + 'req/20')
        self.assertEqual(response.json(), get_cmp)

    def step_put(self):
        response = requests.put(BASE + 'req/29', put_request)
        self.assertEqual(response.json(), put_cmp)

    def step_patch(self):
        response = requests.patch(BASE + 'req/29', patch_request)
        self.assertEqual(response.json(), patch_cmp)

    def step_delete(self):
        response = requests.delete(BASE + 'req/29')
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
                self.fail(f'Request {name} failed, check logs/tests.log for additional information')
