from flask import Flask, request, jsonify, abort
from .models import FoodItems, TheFood, db
from sqlalchemy.orm import joinedload
import json
from my_app import app
from .auth import AuthError, requires_auth




# from .auth.auth import AuthError, requires_auth

@app.route('/')
def home() :
  login = "<a href='https://moaz.uk.auth0.com/authorize?audience=restaurant&response_type=token&client_id=DribS2kVibf9SFkcTFNmOoTWQTNA1WwD&redirect_uri=https://capstone-for-nd-udacity.onrender.com/'>Log in here</a>"
  return login

@app.route('/the-food-detail')
@requires_auth('get:data')
def get_drinks(payload) :
  the_food = db.session.query(TheFood).join(FoodItems).filter(FoodItems.id == TheFood.rate_it).all()
  the_food_list = [{'id': item.id, 'name': item.name, 'type': item.food_item.type} for item in the_food]
  # return data in user
  return jsonify({
    'success': True,
    'the_food': the_food_list
  })

@app.route('/food-items-detail')
@requires_auth('get:data')
def get_food_items_detail(payload) :
  # get data in database
  food_items = FoodItems.query.all()
  # return data in list
  food_items_list = [{'id': item.id, 'type': item.type} for item in food_items]
  # return data in user
  return jsonify({
    'success': True,
    'food_items': food_items_list
  })

@app.route('/the-food', methods=['POST'])
@requires_auth('post:data')
def create_the_food(payload) :
  #get data in link
  data = request.get_json()
  name = data.get('name')
  rate_it = data.get('rate_it')
  # check if title already exists in the database
  if TheFood.query.filter_by(name=name).first():
    abort(409) 
  if not FoodItems.query.get(rate_it):
    abort(400)  # Bad request - rate_it doesn't exist
  #check data
  if not name :
    abort(400)
  elif not rate_it :
    abort(400)
  else :
  # add data in database
    the_food = TheFood(name=name, rate_it=rate_it)
    the_food.insert()

    the_food_get = db.session.query(TheFood).join(FoodItems).filter(FoodItems.id == TheFood.rate_it).all()
    the_food_list = [{'id': item.id, 'name': item.name, 'type': item.food_item.type} for item in the_food_get]

    return jsonify({
      'success': True,
      'the_food': the_food_list
    })

@app.route('/food-items', methods=['POST'])
@requires_auth('post:data')
def create_food_items(payload) :
  #get data in link
  data = request.get_json()
  type = data.get('type')
  # check if title already exists in the database
  existing_food_items = FoodItems.query.filter_by(type=type).first()
  if existing_food_items:
    abort(409)  # Conflict - title already exists
  #check data
  if not type :
    abort(400)
  else :
    # add data in database
    food_items = FoodItems(type=type)
    food_items.insert()
    food_items_get = FoodItems.query.all()
    food_items_list = [{'id': item.id, 'type': item.type} for item in food_items_get]
    # return data in user
    return jsonify({
    'success': True,
    'food_items': food_items_list
    })



@app.route('/the-food/<int:id>', methods=['PATCH'])
@requires_auth('patch:data')
def update_the_food(payload, id):
  #get data in link
  data = request.get_json()
  name = data.get('name')
  rate_it = data.get('rate_it')
  # get data in database
  the_food = TheFood.query.get(id)
  #check data
  if not the_food:
    abort(404)
  if name:
    the_food.name = name
  if rate_it:
    the_food.rate_it = rate_it
  # update data
  the_food.update()
  # return data in user
  the_food_get = db.session.query(TheFood).join(FoodItems).filter(FoodItems.id == TheFood.rate_it).all()
  the_food_list = [{'id': item.id, 'name': item.name, 'type': item.food_item.type} for item in the_food_get]
  return jsonify({
    'success': True,
    'the_food': the_food_list
  })

@app.route('/food-items/<int:id>', methods=['PATCH'])
@requires_auth('patch:data')
def update_food_items(payload, id):
  #get data in link
  data = request.get_json()
  type = data.get('type')

  # get data in database
  food_items = FoodItems.query.get(id)
  #check data
  if not food_items:
    abort(404)
  if type:
    food_items.type = type
  # update data
  food_items.update()
  # return data in user
  return jsonify({
    'success': True,
    'food_items': [{'id': item.id, 'type': item.type} for item in FoodItems.query.all()]
  })

@app.route('/the-food/<int:id>', methods=['DELETE'])
@requires_auth('delete:data')
def delete_the_food(payload, id):
  # get data in database
  the_food = TheFood.query.get(id)
  # check data
  if not the_food:
    abort(404)
  else :
    #delete data
    the_food.delete()
    # return data in user
    return jsonify({
      'success': True,
      'delete': id
    }), 200

@app.route('/food-items/<int:id>', methods=['DELETE'])
@requires_auth('delete:data')
def delete_food_items(payload, id):
  # get data in database
  food_items = FoodItems.query.get(id)
  # check data
  if not food_items:
    abort(404)
  else :
    #delete data
    food_items.delete()
    # return data in user
    return jsonify({
      'success': True,
      'delete': id
    }), 200

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
    "success": False,
    "error": 422,
    "message": "unprocessable"
  }), 422

@app.errorhandler(404)
def not_found(error):
  return jsonify({
    "success": False,
    "error": 404,
    "message": "resource not found"
  }), 404

@app.errorhandler(400)
def not_processed(error):
  return jsonify({
    "success": False,
    "error": 400,
    "message": "This transaction cannot be processed"
  }), 400

@app.errorhandler(409)
def not_insert_data(error):
  return jsonify({
    "success": False,
    "error": 409,
    "message": "It is not possible to add data to a name in the database"
  }), 409

@app.errorhandler(AuthError)
def auth_error(error):
  return jsonify({
    "success": False,
    "error": error.status_code,
    "message": error.error
  }), error.status_code