from sqlalchemy import select
from Models import User
from flask_sqlalchemy import SQLAlchemy

def get_user(db:SQLAlchemy, user_id:int) -> User:
    qry = select(User).where(User.id == user_id)
    return db.session.execute(qry).scalars().one_or_none()