# Account details user > change password (siaip is login) +
# my_orders > create review +
# my reviews +
# my_blance
# logout

from app import db
from Models.order import Order
from Models.user import User
from Models.order_item import Order_item
from Models.review import Review
from Models.payment import Payment
from Models.wallet_transaction import Wallet_transaction
from sqlalchemy import func, select
from Misc.decorators import handle_errors

# from Misc.constants import ORDER_STATUSES


@handle_errors(default_return=None, flash_message="Failed to get User.")
def get_login_user(user_id):
    user = User.query.get_or_404(user_id)
    return user


@handle_errors(default_return=None, flash_message="Failed to edit User.")
def edit_user(user_id, form):
    user = User.query.get_or_404(user_id)
    # user.email = form.email.data
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    if password := form.password.data:
        user.password = password
    db.session.commit()


@handle_errors(default_return=([], None), flash_message="Failed to get User Orders.")
def get_user_orders_by_id(user_id):
    orders = db.session.execute(
        select(
            Order.id,
            Order.status,
            func.round(Order.total_amount, 2).label('total_amount'),
            func.date(Order.created_at).label('created_at'),
            Order.loyalty_discount,
            User.email.label('email'),
            func.sum(Order_item.qty).label("total_qty"),
            func.count(Order_item.id).label('count_items'),
            func.count(Review.id).label("count_reviews")

        ).join(User, Order.user_id == User.id)
        .join(Order_item, Order.id == Order_item.order_id)
        .outerjoin(Review, Review.order_item_id == Order_item.id)
        .where(Order.user_id == user_id)
        .group_by(Order.id, Order.status, Order.total_amount, Order.created_at, User.email)
        .order_by(Order.created_at.desc(), Order.total_amount.desc())
    ).all()
    total_sale = sum(item.total_amount for item in orders)
    return orders, total_sale


@handle_errors(default_return=None, flash_message="Failed to get User Balance.")
def get_user_balance(user_id):
    """_summary_
    get user balance by user id
    Args:
        user_id (int): _description_

    Returns:
       Float: formated float
    """
    wallet_sum = db.session.execute(
        select(
            func.sum(Wallet_transaction.amount).label('sum_amount')
        ).where(Wallet_transaction.user_id == user_id)
    ).scalar() or 0

    # wallet_sum = db.session.execute(
    #     select(
    #         Wallet_transaction.user_id,
    #         func.sum(Wallet_transaction.amount).label('sum_amount')
    #     ).outerjoin(User.wallet_transactions)
    #     .where(Wallet_transaction.user_id == user_id)
    #     .group_by(Wallet_transaction.user_id)
    # ).first()

    # only where order status is Pending or Done
    expenses = get_user_expenses(user_id)
    expense_amount = getattr(expenses, 'expence_amount', 0)

    return round(wallet_sum - expense_amount, 2)


@handle_errors(default_return=None, flash_message="Failed to get User Balance.")
def add_balance(user_id, amount):
    wallet_transaction = Wallet_transaction(user_id=user_id, amount=amount)
    db.session.add(wallet_transaction)
    db.session.commit()


@handle_errors(default_return=None, flash_message="Failed to get User Balance.")
def add_balance_stripe(user_id, amount, session_id):
    amount = amount/100
    payment = Payment(user_id=user_id, amount=amount,
                      session_id=session_id, status='success', currency='eur')
    wallet_transaction = Wallet_transaction(user_id=user_id, amount=amount)
    db.session.add(payment)
    db.session.add(wallet_transaction)
    db.session.commit()


# shared function
def get_user_expenses(user_id):
    expenses = db.session.execute(
        select(
            Order.user_id,
            func.sum(Order.total_amount).label('expence_amount')
        ).where(Order.user_id == user_id, Order.status.in_(['Pending', 'Done']))
        .group_by(Order.user_id)
    ).first()

    return expenses
