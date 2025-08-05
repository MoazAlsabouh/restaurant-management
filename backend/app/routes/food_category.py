from flask import request, jsonify, abort
from app.models import FoodCategory
from app.extensions import db
from app.auth.auth import requires_auth

from flask import Blueprint
food_category_bp = Blueprint('the_food_bp', __name__)

@food_category_bp.route('/', methods=['POST'])
@requires_auth(['admin', 'manager'])
def create_food_category(payload):
    data = request.get_json()
    type = data.get('type')
    if FoodCategory.query.filter_by(type=type).first():
        abort(409)
    if not type:
        abort(400)
    food_category = FoodCategory(type=type)
    food_category.insert()
    food_category_list = [{'id': item.id, 'type': item.type} for item in FoodCategory.query.all()]
    return jsonify({
        'success': True,
        'food_items': food_category_list
    })

@food_category_bp.route('/detail')
@requires_auth(['user' ,'admin', 'manager'])
def get_food_category_detail(payload):
    food_category = FoodCategory.query.all()
    food_category_list = [{'id': item.id, 'type': item.type} for item in food_category]
    return jsonify({
        'success': True,
        'food_items': food_category_list
    })


@food_category_bp.route('/<int:id>', methods=['PATCH'])
@requires_auth(['admin', 'manager'])
def update_food_category(payload, id):
    data = request.get_json()
    type = data.get('type')
    food_category = FoodCategory.query.get(id)
    if not food_category:
        abort(404)
    if type:
        food_category.type = type
    food_category.update()
    return jsonify({
        'success': True,
        'food_items': [{'id': item.id, 'type': item.type} for item in FoodCategory.query.all()]
    })

@food_category_bp.route('/<int:id>', methods=['DELETE'])
@requires_auth(['manager'])
def delete_food_category(payload, id):
    food_category = FoodCategory.query.get(id)
    if not food_category:
        abort(404)
    food_category.delete()
    return jsonify({
        'success': True,
        'delete': id
    }), 200
