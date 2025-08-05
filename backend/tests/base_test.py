import os
import unittest
from app import create_app
from app.models import db
from dotenv import load_dotenv

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_database.db"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.init_app(self.app)
        db.create_all()

        self.client = self.app.test_client()

        self.manager_token = os.environ.get("MANAGER_TOKEN")
        self.barista_token = os.environ.get("BARISTA_TOKEN")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
