from flask import Blueprint, request, jsonify, current_app , redirect, url_for, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.oauth import oauth
from app.models.user import User
from app.extensions import db
from datetime import datetime, timedelta
import random
import string
from app.auth.utils import send_email_verification_code, send_activation_link, generate_token
import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv('FRONTEND_URL')

auth_bp = Blueprint('auth', __name__)

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_unique_username(base_username):
    username = base_username
    counter = 1
    while User.query.filter_by(username=username).first():
        username = f"{base_username}{counter}"
        counter += 1
    return username

# تسجيل مستخدم جديد
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    full_name = data.get('full_name')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({"success": False, "message": "جميع الحقول مطلوبة"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "البريد الإلكتروني مستخدم مسبقًا"}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "اسم المستخدم مستخدم مسبقًا"}), 409


    verification_code = generate_verification_code()
    user = User(email=email, username=username, full_name=full_name, email_verification_code=verification_code)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    send_email_verification_code(email, verification_code)

    token = generate_token(user)
    send_activation_link(user.email, token)

    return jsonify({"success": True, "message": "تم التسجيل بنجاح. تحقق من بريدك الإلكتروني."}), 201

# التحقق من البريد الإلكتروني
@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if not email or not code:
        return jsonify({"success": False, "message": "البريد الإلكتروني والرمز مطلوبان"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or user.email_verification_code != code:
        return jsonify({"success": False, "message": "رمز غير صحيح أو المستخدم غير موجود"}), 400

    user.is_verified = True
    user.email_verification_code = None
    db.session.commit()

    return jsonify({"success": True, "message": "تم تأكيد البريد الإلكتروني"}), 200

# تسجيل الدخول والحصول على توكن JWT
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "البريد الإلكتروني وكلمة المرور مطلوبان"}), 400

    user = User.query.filter_by(email=email).first()

    if user.oauth_provider:
        return jsonify({"success": False, "message": f"يرجى تسجيل الدخول باستخدام {user.oauth_provider}"}), 403
    
    if user is None or not user.check_password(password):
        return jsonify({"success": False, "message": "بيانات الدخول غير صحيحة"}), 401
    
    if not user.is_verified:
        return jsonify({"success": False, "message": "يرجى تأكيد بريدك الإلكتروني أولاً"}), 403

    token = generate_token(user)

    return jsonify({"success": True, "token": token}), 200

@auth_bp.route('/activate/<token>', methods=['GET'])
def activate_account(token):
    from jwt import decode, ExpiredSignatureError, InvalidTokenError

    try:
        payload = decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        user_id = payload.get("user_id")
    except ExpiredSignatureError:
        return jsonify({"success": False, "message": "انتهت صلاحية الرابط"}), 400
    except InvalidTokenError:
        return jsonify({"success": False, "message": "رابط غير صالح"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "المستخدم غير موجود"}), 404

    user.is_verified = True
    db.session.commit()

    return jsonify({"success": True, "message": "تم تفعيل الحساب بنجاح"}), 200



@auth_bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"success": False, "message": "البريد الإلكتروني مطلوب"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": True, "message": "إذا كان البريد موجودًا، سيتم إرسال التعليمات إليه"}), 200

    code = generate_verification_code()
    user.reset_password_code = code
    user.reset_code_expires_at = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    send_email_verification_code(user.email, code)

    return jsonify({"success": True, "message": "تم إرسال رمز إعادة تعيين كلمة المرور"}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('new_password')

    if not email or not code or not new_password:
        return jsonify({"success": False, "message": "البيانات ناقصة"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or user.reset_password_code != code:
        return jsonify({"success": False, "message": "رمز غير صحيح"}), 400

    if datetime.utcnow() > user.reset_code_expires_at:
        return jsonify({"success": False, "message": "انتهت صلاحية الرمز"}), 400

    user.set_password(new_password)
    user.reset_password_code = None
    user.reset_code_expires_at = None
    db.session.commit()

    return jsonify({"success": True, "message": "تم تعيين كلمة المرور الجديدة"}), 200

# بداية تسجيل الدخول لمزود جوجل
@auth_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.authorize_google', _external=True) # هذا يكون http://localhost:5000/api/v1/auth/authorize/google
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize/google')
def authorize_google():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.userinfo()  # تحصل معلومات المستخدم من API جوجل مباشرة
    email = user_info.get('email')
    base_username = email.split('@')[0]
    username = generate_unique_username(base_username)
    full_name = user_info.get('name')

    user = User.query.filter_by(email=email).first()
    if user:
        if user.oauth_provider != 'google':
            message = f"تم تسجيل هذا البريد عبر {user.oauth_provider}. لا يمكنك تسجيل الدخول باستخدام Google."
            return redirect(f"{FRONTEND_URL}/auth/callback?error={message}")
    else:
        user = User(email=email, username=username, full_name=full_name, is_verified=True, oauth_provider='google')
        user.set_password(generate_verification_code(12))  # كلمة مرور عشوائية
        db.session.add(user)
        db.session.commit()

    access_token = generate_token(user)
    return redirect(f"{FRONTEND_URL}/auth/callback?token={access_token}")

# فيسبوك
@auth_bp.route('/login/facebook')
def login_facebook():
    redirect_uri = url_for('auth.authorize_facebook', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize/facebook')
def authorize_facebook():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('me?fields=id,name,email')
    user_info = resp.json()
    email = user_info.get('email')
    base_username = email.split('@')[0]
    username = generate_unique_username(base_username)
    full_name = user_info.get('name')

    user = User.query.filter_by(email=email).first()

    if user:
        if user.oauth_provider != 'facebook':
            message = f"تم تسجيل هذا البريد عبر {user.oauth_provider}. لا يمكنك تسجيل الدخول باستخدام facebook."
            return redirect(f"{FRONTEND_URL}/auth/callback?error={message}")
    else :
        user = User(email=email, username=username, full_name=full_name, is_verified=True, oauth_provider='facebook')
        user.set_password(generate_verification_code(12))  # كلمة مرور عشوائية
        db.session.add(user)
        db.session.commit()

    access_token = generate_token(user)
    return redirect(f"{FRONTEND_URL}/auth/callback?token={access_token}")

# جتهاب GitHub
@auth_bp.route('/login/github')
def login_github():
    redirect_uri = url_for('auth.authorize_github', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize/github')
def authorize_github():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user')
    user_info = resp.json()
    email = user_info.get('email')
    # جتهاب ممكن ما يعطينا الإيميل مباشرة، في حالات نحتاج نجلبه من API تاني
    if not email:
        emails_resp = oauth.github.get('user/emails')
        emails = emails_resp.json()
        primary_emails = [e['email'] for e in emails if e['primary'] and e['verified']]
        email = primary_emails[0] if primary_emails else None

    if not email:
        return jsonify({"success": False, "message": "لم يتم الحصول على البريد الإلكتروني من GitHub"}), 400

    base_username = email.split('@')[0] or user_info.get('login')
    username = generate_unique_username(base_username)
    full_name = user_info.get('name') or user_info.get('login')

    user = User.query.filter_by(email=email).first()

    if user :
        if user.oauth_provider != 'github' :
            message = f"تم تسجيل هذا البريد عبر {user.oauth_provider}. لا يمكنك تسجيل الدخول باستخدام github."
            return redirect(f"{FRONTEND_URL}/auth/callback?error={message}")
    else :
        user = User(email=email, username=username, full_name=full_name, is_verified=True, oauth_provider='github')
        user.set_password(generate_verification_code(12))  # كلمة مرور عشوائية
        db.session.add(user)
        db.session.commit()

    access_token = generate_token(user)
    return redirect(f"{FRONTEND_URL}/auth/callback?token={access_token}")