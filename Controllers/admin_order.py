# Perziureti visus user order ir statusus
# Order galima editinti ir istrinti
# Keisti order status
# Kai pasikeicia statusas daromas patikrinimas del user Loyalty
# Kai pasikeicia statusas nusiskaiciuoja balansas
# Perziureti orderiu Items ir juos ivertinti (comment ir rating star)

from app import db
from Models.order import Order
from Models.user import User
from Models.order_item import Order_item
from Models.review import Review
from sqlalchemy import func, select
from Misc.constants import ORDER_STATUSES

# ka issivesti

# id, status, total_amount, created_at, user.email, sum order_item.qty, count review, link_to_order


def get_orders():
    orders = db.session.query(
        Order.id,
        Order.status,
        func.round(Order.total_amount, 2).label('total_amount'),
        func.date(Order.created_at).label('created_at'),
        Order.loyalty_discount,
        User.email.label('email'),
        func.sum(Order_item.qty).label("total_qty"),
        func.count(Review.id).label("count_reviews")

    ).join(User, Order.user_id == User.id) \
        .join(Order_item, Order.id == Order_item.order_id) \
        .outerjoin(Review, Review.order_item_id == Order_item.id) \
        .group_by(Order.id, Order.status, Order.total_amount, Order.created_at, User.email) \
        .order_by(Order.created_at.desc(), Order.total_amount.desc()) \
        .all()
    total_sale = sum(item.total_amount for item in orders)
    return orders, total_sale


# User email
# Order items all
# id, order_id, product_id, gty, product_name, unit_price, total_amount, created_at, review.id, review.rating, review.content

def get_order_items(order_id):
    order_items = db.session.query(
        Order_item.id,
        Order_item.order_id,
        Order_item.product_id,
        Order_item.qty,
        Order_item.product_name,
        func.round(Order_item.unit_price, 2).label('unit_price'),
        func.round(Order_item.total_price, 2).label('total_price'),
        Order_item.created_at,
        Review.id.label("review_id"),
        Review.rating.label("rating"),
        Review.content.label("content")
    ) \
        .outerjoin(Review, Review.order_item_id == Order_item.id) \
        .filter(Order_item.order_id == order_id) \
        .all()

    order = get_order_with_user_by_id(order_id)

    return order_items, order, ORDER_STATUSES


def get_item_review(item_id):
    item = db.session.execute(
        select(
            Review.id,
            Review.order_item_id,
            Review.rating,
            Review.content,
            Order_item.product_name,
            Order_item.id.label('item_id'),
            Order_item.order_id.label('order_id'),
            func.date(Order_item.created_at).label('created_at'),
            func.round(Order_item.unit_price, 2).label('unit_price'),
            func.round(Order_item.qty, 2).label('qty'),
            func.round(Order_item.total_price, 2).label('total_price'),
            func.date(Order_item.created_at).label('created_at'),
        ).outerjoin(Order_item.reviews)
        .where(Order_item.id == item_id)
    ).first()

    order = get_order_with_user_by_id(item.order_id)

    return item, order


def set_order_status(order_id, status):
    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()
    else:
        raise Exception("Order not found")


def set_review(item_id, rating, content):
    review = Review.query.filter(Review.order_item_id == item_id).first()
    if review:
        review.rating = rating
        review.content = content
        db.session.commit()
    else:
        review = Review(rating=rating, content=content, order_item_id=item_id)
        db.session.add(review)
        db.session.commit()
        # raise Exception("Review not found")


def remove_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
    else:
        raise Exception("Review not found")

# shared function


def get_order_with_user_by_id(order_id):
    order = db.session.execute(select(
        Order.id,
        Order.status,
        Order.loyalty_discount,
        func.round(Order.total_amount, 2).label('total_amount'),
        Order.total_amount,
        func.date(Order.created_at).label('created_at'),
        User.email.label("email"),
        User.id.label("user_id"),
    )
        .join(Order.user)
        .where(Order.id == order_id)) \
        .first()

    return order
