import unittest
import requests
from logger.logs import BASE, logger
from app import app as tested_app


put_department = {'title': 'Test'}

patch_department = {'title': 'Test2'}

get_cmp = {'id': 2,
           'title': 'Human resources'}

put_cmp = {'id': 8,
           'title': 'Test'}

patch_cmp = {'id': 8,
             'title': 'Test2'}

delete_cmp = patch_cmp


class TestDepartmentRESTAPI(unittest.TestCase):
    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def step_get(self):
        response = self.app.get('/dep/2')
        #response = requests.get(BASE + 'dep/2')
        self.assertEqual(response.json(), get_cmp)

    def step_put(self):
        response = requests.put(BASE + 'dep/8', put_department)
        self.assertEqual(response.json(), put_cmp)

    def step_patch(self):
        response = requests.patch(BASE + 'dep/8', patch_department)
        self.assertEqual(response.json(), patch_cmp)

    def step_delete(self):
        response = requests.delete(BASE + 'dep/8')
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
                self.fail(f'Department {name} failed, check logs/tests.log for additional information')
