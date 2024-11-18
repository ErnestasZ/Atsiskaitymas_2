from app import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String)
    stock = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # relations
    order_items = db.relationship('Order_item', back_populates='product', cascade="all, delete")
    cart_products = db.relationship('Cart_product', back_populates='product', cascade="all, delete")