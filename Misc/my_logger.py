import logging
from functools import wraps

# nustatom level

my_logger = logging.Logger('app', level=logging.DEBUG)

# output i faila

formatter = logging.Formatter(fmt='{asctime} {filename} [{levelname}]: {message}', style='{')
file_handler = logging.FileHandler("instance/app.log")
file_handler.setFormatter(formatter)
my_logger.addHandler(file_handler)

# output i ekrana pagal custom filtra

def custom_filter(record: logging.LogRecord) -> bool:
    return record.levelno >= logging.WARNING and record.filename == "app.py"
stream_handler = logging.StreamHandler()
stream_handler.addFilter(custom_filter)
stream_handler.setFormatter(formatter)
my_logger.addHandler(stream_handler) 

# naudojimo pavyzdys

# my_logger.debug('debug msg')
# my_logger.info('info msg')
# my_logger.error('error msg')

def log_crud_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            my_logger.info(f'Calling {func.__name__} with arguments: {args}, {kwargs}')
            result = func(*args, **kwargs)
            my_logger.info(f'{func.__name__} completed successfully')
            return result
        except Exception as e:
            my_logger.error(f'{func.__name__} failed with error: {str(e)}')
            raise  # Re-raise the exception after logging
    return wrapper
