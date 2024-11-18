from app import db
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String)
    veryfied_at = db.Column(db.DateTime) # [!] turetu buti verified_at
    is_deleted = db.Column(db.Boolean, default=False)
    blocked_until = db.Column(db.DateTime)
    failed_count = db.Column(db.Integer)
    loyalty_id = db.Column(db.Integer, db.ForeignKey('loyalties.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # relations
    loyalty = db.relationship('Loyalty', back_populates='users')
    orders = db.relationship('Order', back_populates='user')
    cart_products = db.relationship('Cart_product', back_populates='user')
    wallet_transactions = db.relationship('Wallet_transaction', back_populates='user')
    # methods for password hash
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    # methods for flask_login
    @property
    def is_active(self):
        return (not self.is_deleted) and ((self.blocked_until is None) or (self.blocked_until < datetime.now()))
    # methods for token
    def generate_token(self):
        return secrets.token_urlsafe(16)  # Generates a secure, URL-safe token
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.token:
            self.token = self.generate_token()    
