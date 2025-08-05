# routes/admin.py
from flask import Blueprint, jsonify, request
from app.models.user import User
from app.auth.auth import requires_auth
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@requires_auth(['admin', 'manager'])
def get_users(payload):
    query = User.query
    # الفلاتر المدعومة
    email = request.args.get('email')
    role = request.args.get('role')
    is_active = request.args.get('is_active')
    full_name = request.args.get('full_name')
    username = request.args.get('username')

    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if role:
        query = query.filter_by(role=role)
    if is_active is not None:
        is_active_bool = is_active.lower() == 'true'
        query = query.filter_by(is_active=is_active_bool)
    if full_name:
        query = query.filter(User.full_name.ilike(f"%{full_name}%"))
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))

    users = query.all()
    users_list = [{
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat()
    } for user in users]

    return jsonify({"success": True, "users": users_list})

@admin_bp.route('/user/<int:user_id>', methods=['GET'])
@requires_auth(['admin', 'manager'])
def get_user_by_id(payload, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found",
            "status_code": 404
        }), 404

    user_data = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat()
    }

    return jsonify({
        "success": True,
        "user": user_data
    })

@admin_bp.route('/user/<int:user_id>/role', methods=['PATCH'])
@requires_auth(['manager'])
def update_user_role(payload, user_id):
    data = request.get_json()
    new_role = data.get('role')

    # تحقق من صحة الدور المطلوب
    if new_role not in ['user', 'admin']:
        return jsonify({
            "success": False,
            "error": "Invalid role. Allowed roles: 'user', 'admin'",
            "status_code": 400
        }), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found",
            "status_code": 404
        }), 404

    old_role = user.role
    user.role = new_role
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Role updated from '{old_role}' to '{new_role}' for user ID {user_id}"
    })

@admin_bp.route('/user/<int:user_id>/username', methods=['PATCH'])
@requires_auth(['admin', 'manager'])
def update_username(payload, user_id):
    data = request.get_json()
    new_username = data.get('username')

    if not new_username or len(new_username) < 3:
        return jsonify({
            "success": False,
            "error": "Username must be at least 3 characters long",
            "status_code": 400
        }), 400

    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user and existing_user.id != user_id:
        return jsonify({
            "success": False,
            "error": "Username already taken",
            "status_code": 409
        }), 409

    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found",
            "status_code": 404
        }), 404

    old_username = user.username
    user.username = new_username
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Username updated from '{old_username}' to '{new_username}' for user ID {user_id}",
        "user": {
            "id": user.id,
            "old_username": old_username,
            "new_username": new_username
        }
    })

@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@requires_auth(['manager'])
def delete_user(payload, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found",
            "status_code": 404
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"User with ID {user_id} has been deleted"
    })

@admin_bp.route('/user/<int:user_id>/toggle-active', methods=['PUT'])
@requires_auth(['admin', 'manager'])
def toggle_user_active(payload, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    user.is_active = not user.is_active
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"User {'activated' if user.is_active else 'deactivated'} successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active
        }
    })

@admin_bp.route('/user/<int:user_id>/activate', methods=['PUT'])
@requires_auth(['admin', 'manager'])
def activate_user(payload, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    user.is_active = True
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User account activated",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active
        }
    })
