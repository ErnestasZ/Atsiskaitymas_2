from Models import User
def get_users(db) -> list[User] | None:
    ...

def get_user_by_id(db, user_id:int) -> User:
    ...

def get_user_by_email(db, email:str) -> User:
    ...

def update_user(db, user:User) -> True | str:
    """
    Returns [bool]True if user updated successfully 
    Returns [str] error message if update failed
    """
    ...

def create_user(db, user:User) -> True | str:
    """
    Returns [bool]True if user created successfully 
    Returns [str] error message if create failed
    """
    ...

def add_to_wallet(db, user_id:int, amount:float) -> True | str:
    """
    Returns [bool]True if added successfully 
    Returns [str] error message if add failed
    """
    ...

def get_user_balance(db, user_id:int) -> float:
    ...
