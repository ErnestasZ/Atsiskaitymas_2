from app import db

class Cart_product(db.Model):
    __tablename__ = 'cart_products'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    qty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # relations
    user = db.relationship('User', back_populates='cart_products')
    product = db.relationship('Product', back_populates='cart_products')