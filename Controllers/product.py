from Models import Product

def get_products(db, sort:dict[str:str], name:str=None, price:list[float:float]=None) -> list[Product]:
    """
    sort(dict) key[str]- parameter that is used for sorting
    value[str]- ASC|DESC
    """
    ...

def update_product(db, product:Product) -> bool | str:
    """
    Returns [bool] True on success
    Returns [str] error message on fail
    """
    ...