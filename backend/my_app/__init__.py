from flask import Flask
from my_app.models import setup_db, db_drop_and_create_all
from flask_cors import CORS
import os
from dotenv import load_dotenv




def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    load_dotenv()
    return app

app = create_app()

with app.app_context(): 
    db_drop_and_create_all()

from my_app import routes