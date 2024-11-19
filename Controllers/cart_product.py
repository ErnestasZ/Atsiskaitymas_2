from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from Models import Cart_product
from Misc.my_logger import my_logger, log_crud_operation
import uuid

# Temporary Session ID
def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@log_crud_operation
def add_cart_product(db:SQLAlchemy, cart_product:Cart_product) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    try:
        db.session.add(cart_product)
        db.session.commit()
        return True
    except Exception as e:
        msg = f"An error occurred while adding to cart: {str(e)}"
        my_logger.error(msg)
        db.session.rollback()
        return msg

def drop_cart(db, user_id:int = None) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def update_cart_product(db:SQLAlchemy, cart_product:Cart_product) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    qry = select(Cart_product).where(car)

def delete_cart_product(db, cart_product:Cart_product) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...
def validate_cart(db, session_id:int, user_id:int = None) -> None:
    """
    Function validates cart. Checks if items in cart still exist and there is enough stock
    """

def get_cart(db:SQLAlchemy, session_id:int, user_id:int = None) -> list[Cart_product]:
    """
    Returns [list]Cart_product
    """
    qry = select(Cart_product)
    if user_id:
        qry = qry.where(Cart_product.user_id == user_id)
    else:
        qry = qry.where(Cart_product.session_id == session_id).where(Cart_product.user_id == None)
    
    return db.session.execute(qry).scalars().all()

def get_cart_product(db:SQLAlchemy, session_id:int, product_id:int, user_id:int = None) -> Cart_product:
    """
    Returns [list]Cart_product
    """
    qry = select(Cart_product)
    if user_id:
        qry = qry.where(Cart_product.user_id == user_id)
    else:
        qry = qry.where(Cart_product.session_id == session_id).where(Cart_product.user_id == None)

    qry = qry.where(Cart_product.product_id == product_id)
    print(qry)
    return db.session.execute(qry).scalars().one_or_none()
    

    