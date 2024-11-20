from Models import User, Order, Wallet_transaction
from Controllers import db_provider as dbp
from Misc.my_logger import log_crud_operation

@log_crud_operation
def make_payment(user: User, order: Order) -> (Wallet_transaction | Exception):
    paiment = dbp.push_db_record(Wallet_transaction, user_id=user.id, amount=order.total_amount * -1)
    
    if isinstance(paiment, Wallet_transaction):
        dbp.push_db_record(order, status="Paid")
    return paiment