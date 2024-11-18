from Models import User, Loyalty
from Misc.my_logger import my_logger
from datetime import datetime, timezone

def get_users(db) -> list[User]:
    return db.session.query(User).all()


def create_user(db, user: User) -> bool | str:
    try:
        db.session.add(user)
        db.session.commit()
        my_logger.info(f'create {user.id} success')
        return True
    except Exception as e:
        db.session.rollback()
        my_logger.info(f'create {user.id} failed: {str(e)}')
        return str(e)


def verify_user_token(db, token: str) -> bool | str:
    try:
        user = User.query.filter_by(token=token).first()
        if user:
            user.verified_at = datetime.now(timezone.utc)
            db.session.flush()
            db.session.commit()
            my_logger.info(f'verification of token {token} success')
            return True
        my_logger.info(f'verification of token {token} failed')
        return 'Invalid or expired token!'
    except Exception as e:
        db.session.rollback()
        my_logger.info(f'verification of token {token} failed: {str(e)}')
        return str(e)


def get_user_by_id(db, user_id: int) -> User:
    return db.session.query(User).filter_by(id=user_id).first()


def get_user_by_email(db, user_email: str) -> User:
    return db.session.query(User).filter_by(email=user_email).first()


def update_user(db, user: User) -> bool | str:
    try:
        existing_user = db.session.query(User).filter(User.id == user.id).first()
        if not existing_user:
            return 'User not found'
        for key, value in user.__dict__.items():
            if not key.startswith('_'):
                setattr(existing_user, key, value)
        db.session.flush()
        db.session.commit()
        my_logger.info(f'update {user.id} success')
        return True
    except Exception as e:
        db.session.rollback()
        my_logger.info(f'update {user.id} failed: {str(e)}')
        return str(e)


def add_to_wallet(db, user_id:int, amount:float) -> bool | str:
    """
    Returns [bool]True if added successfully 
    Returns [str] error message if add failed
    """
    ...


def get_user_balance(db, user_id:int) -> float:
    ...
