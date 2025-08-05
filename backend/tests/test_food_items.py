import json
from .base_test import BaseTestCase
from app.models import FoodItems

class FoodItemsTestCase(BaseTestCase):

    new_food_item = {
        'type': 'fast food'
    }

    def test_get_food_items_success(self):
        res = self.client.get('/food-items-detail', headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])
        self.assertTrue(len(data['food_items']) >= 0)

    def test_get_food_items_failure(self):
        res = self.client.get('/food-items-detail')
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_create_food_item_success(self):
        res = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_create_food_item_failure(self):
        res = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_update_food_item_success(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/food-items/1', json={'type': 'Dessert'}, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_update_food_item_failure(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/food-items/1', json={'type': 'Dessert'}, headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_delete_food_item_success(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/food-items/1', headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_delete_food_item_failure(self):
        self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/food-items/1', headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])
