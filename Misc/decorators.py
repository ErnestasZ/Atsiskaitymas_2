from functools import wraps
from flask import flash, current_app
from Misc.my_logger import my_logger


def handle_errors(default_return=None, flash_message="An error occurred!", flash_option='main'):
    """
    A decorator to handle errors in functions.
    Logs errors and optionally flashes a message to the user.

    :param default_return: Default value to return on exception.
    :param flash_message: Message to flash if an exception occurs, if None flash not occurs.
    :param flash_option: for admin or main, default main.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                results = func(*args, **kwargs)
                my_logger.info(f"{func.__name__} executed successfuly")
                return results
            except Exception as e:
                # Log the error
                my_logger.error(f"Error in {func.__name__}: {e}")
                # Flash a user-friendly message
                if flash_message:
                    flash(flash_message, f'{flash_option} danger')
                # Return a default value
                return default_return
        return wrapper
    return decorator
