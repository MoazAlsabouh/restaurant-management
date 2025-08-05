import json
from .base_test import BaseTestCase
from app.models import TheFood

class TheFoodTestCase(BaseTestCase):

    new_food_item = {
        'type': 'fast food'
    }

    new_the_food = {
        'name': 'shawrma',
        "rate_it": "1"
    }

    def test_get_the_food_success(self):
        res = self.client.get('/the-food-detail', headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])
        self.assertTrue(len(data['the_food']) >= 0)

    def test_get_the_food_failure(self):
        res = self.client.get('/the-food-detail')
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_create_the_food_success(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_create_the_food_failure(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_update_the_food_success(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/the-food/1', json={'name': 'flafel', 'rate_it': '1'}, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_update_the_food_failure(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/the-food/1', json={'name': 'flafel', 'rate_it': '1'}, headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_delete_the_food_success(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/the-food/1', headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_delete_the_food_failure(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/the-food/1', headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])
