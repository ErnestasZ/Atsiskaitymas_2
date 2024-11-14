from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String)
    veryfied_at = db.Column(db.DateTime)
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