from app import db


class Order_item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    qty = db.Column(db.Integer)
    product_name = db.Column(db.String)
    unit_price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # relations
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='order_items')
    reviews = db.relationship('Review', back_populates='order_item')
