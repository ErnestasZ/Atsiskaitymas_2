from flask_login import current_user
from Models import Loyalty

def get_loyalty_discount():
    """Get the loyalty discount for the current user."""
    if current_user.is_authenticated:
        loyalty = current_user.loyalty
        if loyalty:
            return loyalty.discount
    return 0 
