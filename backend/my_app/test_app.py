import os
import unittest
import json
from flask import request
from my_app import app
from .models import db, setup_db, FoodItems, TheFood
from dotenv import load_dotenv

class RestaurantTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test app
        self.app = app
        self.app_context = self.app.app_context()  # Set up app context
        self.app_context.push()  # Push app context
        self.client = self.app.test_client()
        # Set up a test database
        self.database_name = "test_database.db"
        self.database_path = "sqlite:///{}".format(self.database_name)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.create_all()
        
        # Set up tokens for testing
        self.manager_token = os.environ.get("MANAGER_TOKEN")
        self.barista_token = os.environ.get("BARISTA_TOKEN")

        self.new_food_item = {
            'type': 'fast food'
        }

        self.new_the_food = {
            'name': 'shawrma',
            "rate_it": "1"
        }

    def tearDown(self):
        # Clean up the database after testing
        db.session.remove()
        db.drop_all()

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
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/food-items/1', json={'type': 'Dessert'}, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_update_food_item_failure(self):
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/food-items/1', json={'type': 'Dessert'}, headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_delete_food_item_success(self):
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/food-items/1', headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_delete_food_item_failure(self):
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/food-items/1', headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

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
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_create_the_food_failure(self):
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_update_the_food_success(self):
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        add_data_tf = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/the-food/1', json={'name': 'flafel', 'rate_it': '1'}, headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_update_the_food_failure(self):
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        add_data_tf = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.patch('/the-food/1', json={'name': 'flafel', 'rate_it': '1'}, headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

    def test_manager_can_delete_the_food_success(self):
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        add_data_tf = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/the-food/1', headers={'Authorization': f'Bearer {self.manager_token}'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue(data['success'])

    def test_manager_can_delete_the_food_failure(self):
        # Assuming you have an existing food item with id = 1
        add_data = self.client.post('/food-items', json=self.new_food_item, headers={'Authorization': f'Bearer {self.manager_token}'})
        add_data_tf = self.client.post('/the-food', json=self.new_the_food, headers={'Authorization': f'Bearer {self.manager_token}'})
        res = self.client.delete('/the-food/1', headers={'Authorization': f'Bearer {self.barista_token}'})
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data(as_text=True))
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()
