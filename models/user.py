"""
User Model
"""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """User account"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    
    # Role
    is_admin = db.Column(db.Boolean, default=False)
    
    # Store association
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    
    # Preferences
    notification_email = db.Column(db.Boolean, default=True)
    notification_slack = db.Column(db.Boolean, default=False)
    report_frequency = db.Column(db.String(20), default='weekly')  # daily, weekly, monthly
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'store_id': self.store_id,
            'notification_email': self.notification_email,
            'report_frequency': self.report_frequency,
            'created_at': self.created_at.isoformat()
        }
