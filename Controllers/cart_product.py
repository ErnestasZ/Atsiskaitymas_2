from flask import Flask, session
from Models import Cart_product, User
from Controllers import db_provider as dbp
import uuid

# Temporary Session ID
def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def fill_user(cart: list[Cart_product], user: User) -> None:
    for product in cart:
        if product.user_id:
            continue
        product.user_id = User.id
        dbp.push_db_record(product)

def add_to_cart(db, cart_product:Cart_product) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def drop_cart(cart: list[Cart_product], user: User) -> bool | Exception:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def update_cart_product(db, cart_product:Cart_product) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def delete_cart_product(db, cart_product:Cart_product) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def get_cart(db, session_id:int, user_id:int = None) -> list[Cart_product]:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...