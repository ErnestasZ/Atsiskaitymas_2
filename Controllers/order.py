from Models import Order

def create_order(db, order:Order) -> True|str:
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


def get_order_by_id(db, order_id:int) -> Order | None:
    """
    Returns [bool]True on success 
    Returns [str] error message on fail
    """
    ...

def add_review(db, order_id:int, product_id:int) -> True | str:
    """
    Returns [bool]True on success 
    Returns [str] error message on fail
    """
    ...

