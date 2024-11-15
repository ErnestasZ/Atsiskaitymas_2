from sqlalchemy.orm import Session
from Models import User


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def create_user(db: Session, user: User) -> bool | str:
    try:
        db.add(user)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return str(e)


def get_user_by_id(db: Session, user_id: int) -> User:
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(db: Session, user_email: str) -> User:
    return User.query.filter_by(email=user_email).first()


def update_user(db: Session, user: User) -> bool | str:
    try:
        existing_user = db.query(User).filter(User.id == user.id).first()
        if not existing_user:
            return 'User not found'
        for key, value in user.__dict__.items():
            if not key.startswith('_'):
                setattr(existing_user, key, value)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return str(e)


def add_to_wallet(db: Session, user_id:int, amount:float) -> bool | str:
    """
    Returns [bool]True if added successfully 
    Returns [str] error message if add failed
    """
    ...


def get_user_balance(db: Session, user_id:int) -> float:
    ...
