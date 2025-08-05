from flask import request, jsonify, abort
from app.models import FoodItems, FoodCategory
from app.extensions import db
from app.auth.auth import requires_auth

from flask import Blueprint
food_items_bp = Blueprint('food_items_bp', __name__)


@food_items_bp.route('/', methods=['POST'])
@requires_auth(["admin", "manager"])
def create_food_items(payload):
    data = request.get_json()
    name = data.get('name')
    food_category_id = data.get('food_category_id')
    if FoodItems.query.filter_by(name=name).first():
        abort(409)
    if not FoodCategory.query.get(food_category_id) or not name or not food_category_id:
        abort(400)
    food_items = FoodItems(name=name, food_category_id=food_category_id)
    food_items.insert()
    food_items_get = db.session.query(FoodItems).join(FoodCategory).filter(FoodCategory.id == FoodItems.food_category_id).all()
    food_items_list = [{'id': item.id, 'name': item.name, 'type': item.food_category.type} for item in food_items_get]
    return jsonify({
        'success': True,
        'food_items': food_items_list
    })

@food_items_bp.route('/detail')
@requires_auth(["user", "admin", "manager"])
def get_food_items_detail(payload):
    food_items = db.session.query(FoodItems).join(FoodCategory).filter(FoodCategory.id == FoodItems.food_category_id).all()
    food_items_list = [{'id': item.id, 'name': item.name, 'type': item.food_category.type} for item in food_items]
    return jsonify({
        'success': True,
        'food_items': food_items_list
    })


@food_items_bp.route('/<int:id>', methods=['PATCH'])
@requires_auth(['admin', 'manager'])
def update_food_items(payload, id):
    data = request.get_json()
    name = data.get('name')
    food_category_id = data.get('food_category_id')
    food_items = FoodItems.query.get(id)
    if not food_items:
        abort(404)
    if name:
        food_items.name = name
    if food_category_id:
        food_items.food_category_id = food_category_id
    food_items.update()
    food_items_get = db.session.query(FoodItems).join(FoodCategory).filter(FoodCategory.id == FoodItems.food_category_id).all()
    food_items_list = [{'id': item.id, 'name': item.name, 'type': item.food_category.type} for item in food_items_get]
    return jsonify({
        'success': True,
        'food_items': food_items_list
    })

@food_items_bp.route('/<int:id>', methods=['DELETE'])
@requires_auth(['manager'])
def delete_food_items(payload, id):
    food_items = FoodItems.query.get(id)
    if not food_items:
        abort(404)
    food_items.delete()
    return jsonify({
        'success': True,
        'delete': id
    }), 200
