from app import db
from Models import *

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import DefaultMeta

def create_object(obj: object, **kwargs):
    try:
        new_object = obj(**kwargs)
    except Exception as err:
        new_object = err

    return new_object

def add_db_record(obj: object, session = db.session, **kwargs):

    if isinstance(obj, DefaultMeta): #DeclarativeMeta
        record = create_object(obj, **kwargs)
    else:
        for k, v in kwargs.items(): setattr(obj, k, v)
        record = obj

    if not isinstance(record, Exception):
        try:
            session.add(record)
        except Exception as err:
            session.rollback()
            record = err
        else:
            session.commit()
    return record

# d = db
# prod = Product
print("faefdsfa")
# record = add_db_record()


