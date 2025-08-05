from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=True)  # <-- الاسم الكامل
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # تأكيد البريد الإلكتروني
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    email_verification_code = db.Column(db.String(10), nullable=True)
    # إعادة تعيين كلمة المرور
    reset_password_code = db.Column(db.String(6))
    reset_code_expires_at = db.Column(db.DateTime)
    # أدوار المستخدم
    role = db.Column(db.String(20), default='user')  # roles: user, admin, manager
    oauth_provider = db.Column(db.String(50), nullable=True)  # مثلا: 'google', 'facebook', 'github' أو None
    # تواريخ الإنشاء والتحديث
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_updated_at = db.Column(db.DateTime, nullable=True)


    # دوال المساعدة لتعيين والتحقق من كلمة المرور
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # دالة لتحويل كائن المستخدم إلى قاموس
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }
