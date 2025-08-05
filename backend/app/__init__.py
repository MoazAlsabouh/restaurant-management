from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from .extensions import db, cors
from .models import food_category, food_items
from .routes import register_routes
from .auth.auth import AuthError
from .errors.handlers import register_error_handlers
from .auth.oauth import configure_oauth
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")  # الأفضل تأخذها من .env    load_dotenv()

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    register_routes(app)
    register_error_handlers(app)
    configure_oauth(app)

    return app

app = create_app()