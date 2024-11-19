from app import db
from Models import *
from sqlalchemy.orm import Session

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import DefaultMeta

def pull_db_record(obj: object, statement, session: Session = db.session):
    ...

def pull_db_records(obj: object, statement, session: Session = db.session):
    ...

def create_object(obj: object, **kwargs):
    try:
        new_object = obj(**kwargs)
    except Exception as err:
        new_object = err

    return new_object

def push_db_record(obj: object, session: Session = db.session, **kwargs):

    if isinstance(obj, DefaultMeta):
        record = create_object(obj, **kwargs)
    elif isinstance(obj.__class__, DefaultMeta):
        for k, v in kwargs.items(): setattr(obj, k, v)
        record = obj
    else:
        record = ValueError("The object is not a database object!")

    if not isinstance(record, Exception):
        try:
            session.add(record)
        except Exception as err:
            session.rollback()
            record = err
        else:
            session.commit()
    return record

def delete_db_record(obj: object, session: Session = db.session):
    if isinstance(obj, DefaultMeta):
        try:
            result = session.delete(obj)
        except Exception as err:
            session.rollback()
            result = err
        else:
            session.commit()
    return result
