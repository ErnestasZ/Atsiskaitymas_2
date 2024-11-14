import logging

# nustatom level

my_logger = logging.Logger('app', level=logging.DEBUG)

# output i faila

formatter = logging.Formatter(fmt='{asctime} {filename} [{levelname}]: {message}', style='{')
file_handler = logging.FileHandler("instance/app.log")
file_handler.setFormatter(formatter)
my_logger.addHandler(file_handler)

# output i ekrana

def custom_filter(record: logging.LogRecord) -> bool:
    return record.levelno >= logging.INFO and record.filename == "app.py"
stream_handler = logging.StreamHandler()
stream_handler.addFilter(custom_filter)
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
my_logger.addHandler(stream_handler) 

# naudojimo pavyzdys

# my_logger.debug('debug msg')
# my_logger.info('info msg')
# my_logger.error('error msg')
