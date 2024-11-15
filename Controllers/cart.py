from Models import Cart_product

def add_to_cart(db, cart_product:Cart_product) -> True | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def drop_cart(db, user_id:int = None) -> True | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def update_cart_product(db, cart_product:Cart_product) -> True | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...

def delete_cart_product(db, cart_product:Cart_product) -> True | str:
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