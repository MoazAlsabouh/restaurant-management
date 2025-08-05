from flask import Blueprint
from .food_items import food_items_bp
from .food_category import food_category_bp
from .auth import auth_bp
from .admin import admin_bp
from .profile import profile_bp
from .migrate import migrate_bp


def register_routes(app):
    app.register_blueprint(food_items_bp, url_prefix="/api/v1/food_items")
    app.register_blueprint(food_category_bp, url_prefix="/api/v1/food_category")
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(profile_bp, url_prefix='/api/v1/profile')
    # app.register_blueprint(migrate_bp, url_prefix='/api/v1/migrate')