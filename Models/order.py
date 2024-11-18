from app import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String)
    total_amount = db.Column(db.Float)
    loyalty_discount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # relations
    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('Order_item', back_populates='order')
