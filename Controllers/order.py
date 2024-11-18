from Models import Order
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy

def create_order(db, order:Order) -> bool | str:
    """
    Returns [bool]True on success 
    Returns [str] error message on fail
    """
    ...

def get_orders(db, user_id:int) -> list[Order]:
    """
    Returns [bool]True on success 
    Returns [str] error message on fail
    """
    ...


def get_order_by_id(db:SQLAlchemy, order_id:int) -> Order | None:
    """
    Returns [bool]True on success 
    Returns [str] error message on fail
    """
    qry = select(Order).where(Order.id == order_id)
    return db.session.execute(qry).scalars().one_or_none()

def add_review(db, order_id:int, product_id:int) -> bool | str:
    """
    Returns [bool]True on success 
    Returns [str] error message on fail
    """
    ...

