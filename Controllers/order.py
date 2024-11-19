from sqlalchemy import select, not_, and_, or_
from Models import Order
from Controllers import db_provider as dbp
from Misc.my_logger import log_crud_operation

session = dbp.db.session

@log_crud_operation
def get_order_by_id(id: int) -> (Order | None):
    stmt = select(Order).where(Order.id == id)
    return session.execute(stmt).scalars().first()

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

def add_review(db, order_id:int, product_id:int) -> bool | str:
    """
    Returns [bool]True on success 
    Returns [str] error message on fail
    """
    ...

