from flask import Blueprint, request, jsonify
from app.models.user import User, db
from app.auth.auth import requires_auth
from werkzeug.security import check_password_hash, generate_password_hash

profile_bp = Blueprint('profile_bp', __name__)

# جلب بيانات المستخدم الحالي
@profile_bp.route('/', methods=['GET'])
@requires_auth(['user', 'admin', 'manager'])
def get_my_profile(payload):
    user_id = payload['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    })

# تحديث كلمة المرور
@profile_bp.route('/update-password', methods=['POST'])
@requires_auth(['user', 'admin', 'manager'])
def update_password(payload):
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({"success": False, "message": "كلمة المرور القديمة والجديدة مطلوبة"}), 400

    user_id = payload['user_id']
    user = User.query.get(user_id)

    if not user or not user.check_password(old_password):
        return jsonify({"success": False, "message": "كلمة المرور القديمة غير صحيحة"}), 401

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"success": True, "message": "تم تحديث كلمة المرور بنجاح"}), 200

# تحديث الاسم أو البريد الإلكتروني
@profile_bp.route('/update', methods=['PUT'])
@requires_auth(['user', 'admin', 'manager'])
def update_my_info(payload):
    data = request.get_json()
    user_id = payload['user_id']
    email = data.get('email')
    full_name = data.get('full_name')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    if email:
        user.email = email
    if full_name:
        user.full_name = full_name

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "تم تحديث البيانات بنجاح",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    })

@profile_bp.route('/update-username', methods=['PUT'])
@requires_auth(['user', 'admin', 'manager'])
def update_username(payload):
    data = request.get_json()
    new_username = data.get('username')
    
    if not new_username:
        return jsonify({"success": False, "message": "اسم المستخدم الجديد مطلوب"}), 400

    user_id = payload['user_id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({"success": False, "message": "المستخدم غير موجود"}), 404

    # تحقق من أن اسم المستخدم الجديد غير مستخدم مسبقاً
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user and existing_user.id != user_id:
        return jsonify({"success": False, "message": "اسم المستخدم مستخدم بالفعل"}), 409

    user.username = new_username
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "تم تحديث اسم المستخدم بنجاح",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    })


# حذف (تعطيل) الحساب
@profile_bp.route('/delete', methods=['DELETE'])
@requires_auth(['user', 'admin', 'manager'])
def delete_my_account(payload):
    user_id = payload['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"success": True, "message": "تم تعطيل الحساب بنجاح."})

# عرض معلومات عامة عن أي مستخدم (للمشرفين والمديرين فقط)
@profile_bp.route('/<int:user_id>', methods=['GET'])
@requires_auth(['admin', 'manager'])
def get_user_public_profile(payload, user_id):
    if payload.get("role") not in ["admin", "manager"]:
        return jsonify({"success": False, "error": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user or not user.is_active:
        return jsonify({"success": False, "error": "User not found or inactive"}), 404

    public_info = {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at
    }

    return jsonify({
        "success": True,
        "user": public_info
    })

# اندبوينت عام بدون توثيق لعرض معلومات مستخدم Active (بدون صلاحيات)
@profile_bp.route('/public/<int:user_id>', methods=['GET'])
@requires_auth(['user','admin', 'manager'])
def public_user_profile(user_id):
    user = User.query.get(user_id)
    if not user or not user.is_active:
        return jsonify({"success": False, "error": "User not found or inactive"}), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "role": user.role
        }
    })
