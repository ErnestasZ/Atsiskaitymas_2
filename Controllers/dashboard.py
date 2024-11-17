# Peržiūrėti statistika apie prekes.
# Kiek prekių nupirkta kurią dieną,
# už kiek nupirkta,
# kurie mėnesiai pelningiausi,
# kurios prekės geriausiai įvertintos.
from app import db
from Models.order import Order
from Models.user import User
from Models.review import Review
from Models.order_item import Order_item
from sqlalchemy import func
from datetime import datetime


def get_orders_by_days_in_range(start_date=None, end_date=None):

    orders_query = db.session.query(
        Order.id.label("order_id"),
        Order.created_at.label("created_at"),
        Order.total_amount.label("total_amount"),
        User.email.label("email"),
        func.sum(Order_item.qty).label("total_qty")
    ).join(User, Order.user_id == User.id).join(Order_item, Order.id == Order_item.order_id).order_by(Order.created_at.desc(), Order.total_amount.desc())

    if start_date:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        orders_query = orders_query.filter(Order.created_at >= start_date)

    if end_date:
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        orders_query = orders_query.filter(Order.created_at <= end_date)

    orders_query = orders_query.group_by(Order.id, User.id)

    orders_with_users = orders_query.all()
    total_sale = sum(item.total_amount for item in orders_with_users)
    return orders_with_users, total_sale


def get_order_items_by_days_in_range(start_date=None, end_date=None):

    orders_query = db.session.query(
        Order_item.id.label("item_id"),
        Order_item.product_name.label("title"),
        Order_item.created_at.label("created_at"),
        Order_item.unit_price.label("product_price"),
        # func.sum(Order_item.qty).label("total_qty"),
        # func.sum(Order_item.total_price).label("total")
        Order_item.qty.label("total_qty"),
        Order_item.total_price.label("total"),
        Review.rating.label("rating"),
    ) \
        .outerjoin(Review, Review.order_item_id == Order_item.id)

    if start_date:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        orders_query = orders_query.filter(Order_item.created_at >= start_date)

    if end_date:
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        orders_query = orders_query.filter(Order_item.created_at <= end_date)

    orders_query = orders_query.group_by(Order_item.id).order_by(
        Order_item.created_at.desc(), func.sum(Order_item.total_price).desc())

    # orders_query = orders_query.group_by(Order.id, User.id)
    orders_items = orders_query.all()

    total_sale = sum(item.total for item in orders_items)
    return orders_items, total_sale


def get_sales_by_month():
    month_sales = db.session.query(
        func.strftime('%Y-%m', Order.created_at).label('month'),
        func.sum(Order.total_amount).label('total_amount')
    ) \
        .group_by(func.strftime('%Y-%m', Order.created_at))  \
        .order_by(func.strftime('%Y-%m', Order.created_at)).all()

    return month_sales


def get_best_rated_products():
    best_rated_products = db.session.query(
        Order_item.product_name.label('product_name'),
        Order_item.product_id.label('product_id'),
        Order_item.unit_price.label('price'),
        # Review.rating.label('rating'),
        func.sum(Order_item.qty).label('sales_qty'),
        func.sum(Order_item.total_price).label('total'),
        func.avg(Review.rating).label('average_rating'),
    ) \
        .join(Review, Review.order_item_id == Order_item.id) \
        .group_by(Order_item.product_name, Order_item.product_id) \
        .order_by(func.avg(Review.rating).desc()) \
        .limit(10).all()

    return best_rated_products


def get_best_sales_products():
    best_rated_products = db.session.query(
        Order_item.product_name.label('product_name'),
        Order_item.product_id.label('product_id'),
        Order_item.unit_price.label('price'),
        # Review.rating.label('rating'),
        func.sum(Order_item.qty).label('sales_qty'),
        func.sum(Order_item.total_price).label('total'),
        func.avg(Review.rating).label('average_rating'),
    ) \
        .join(Review, Review.order_item_id == Order_item.id) \
        .group_by(Order_item.product_name, Order_item.product_id) \
        .order_by(func.sum(Order_item.total_price).desc()) \
        .limit(10).all()

    return best_rated_products

# get_orders_by_days_in_range()
# Peržiūrėti statistika apie prekes.
