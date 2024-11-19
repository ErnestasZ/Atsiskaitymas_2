from sqlalchemy import select, not_, and_, or_
from Models import Product, Review, Order_item, Order
from Controllers import db_provider as dbp
from Misc.my_logger import log_crud_operation

session = dbp.db.session

@log_crud_operation
def get_product_by_id(id: int) -> (Product | None):
    stmt = select(Product).where(Product.id == id).where(Product.is_active)
    return session.execute(stmt).scalars().first()

@log_crud_operation
def get_all_products() -> list[Product]:
    return session.execute(select(Product).where(Product.is_active)).scalars().all()

@log_crud_operation
def update_product(id: int = None, product: Product = None, **kwargs) -> (Product | Exception):
    if not product and id:
        product = get_product_by_id(id)
    
    if isinstance(product, Product):
        result = dbp.push_db_record(product, **kwargs)
    else:
        result = ValueError("Unable to update a non-existent database record!")
    return result

@log_crud_operation
def add_product(**kwargs) -> (Product | Exception):
    return dbp.push_db_record(Product, **kwargs)

@log_crud_operation
def get_average_rating(product:Product):
    # Calculate total rating by summing al review ratings product.order_items
    total_rating = sum(review.rating for order_item in product.order_items for review in order_item.reviews if review.rating is not None)
    # Count total num of reviews with rating
    total_reviews = sum(1 for order_item in product.order_items for review in order_item.reviews if review.rating is not None)
    # If total_reviews > 0 count average and round
    if total_reviews > 0:
        average_rating = total_rating / total_reviews
        return round(average_rating, 1)  
    return None

@log_crud_operation
def get_reviews(product:Product):
    reviews = []     # Create empty list of reviews 
    for order_item in product.order_items: 
        for review in order_item.reviews: 
            review.user = order_item.order.user # Link user to review
            reviews.append(review)
    return reviews

def reduce_stock(order: Order):
    ...

@log_crud_operation
def get_products(db, sort: dict[str, str], name: str = None, price: list[float] = None) -> list[Product]:
    """
    Get products from the database with optional sorting, name filtering, and price range.
    :param db: Database session
    :param sort: Dictionary with sort key and direction (ASC or DESC)
    :param name: Optional name filter
    :param price: Optional price range filter [min_price, max_price]
    :return: List of products
    """
    query = db.session.query(Product)

    # Filter by name
    if name:
        query = query.filter(Product.title.ilike(f"%{name}%"))
    
    # Filter by price
    if price:
        min_price, max_price = price
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

    # Start sorting
    if sort:
        for key, direction in sort.items():
            if key == 'default': # Default sorting by name
                query = query.order_by(Product.title.asc())
            elif key == 'rating':  # Sorting by average rating
                query = query.outerjoin(Product.order_items).outerjoin(Order_item.reviews).group_by(Product.id) 
            elif key == 'created_at':  # Sorting by creation date
                if direction.lower() == 'asc':
                    query = query.order_by(Product.created_at.asc())
                elif direction.lower() == 'desc':
                    query = query.order_by(Product.created_at.desc())
            elif key == 'price':  # Sorting by price
                if direction.lower() == 'asc':
                    query = query.order_by(Product.price.asc())
                elif direction.lower() == 'desc':
                    query = query.order_by(Product.price.desc())

    products = query.all()

    # Calculate average rating for each product
    for product in products:
        product.average_rating = get_average_rating(product)

    # Rating for sorting
    if 'rating' in sort:
        products.sort(key=lambda prod: (prod.average_rating is not None, prod.average_rating), reverse=(sort['rating'].lower() == 'desc'))

    return products

def get_sorting_option(sort_option):
    sort = {'key': 'default', 'order': 'asc'}
    
    if sort_option == 'default':
        sort['key'] = 'title'
        sort['order'] = 'asc'
    elif sort_option == 'created_at_asc':
        sort['key'] = 'created_at'
        sort['order'] = 'asc'
    elif sort_option == 'created_at_desc':
        sort['key'] = 'created_at'
        sort['order'] = 'desc'
    elif sort_option == 'price_asc':
        sort['key'] = 'price'
        sort['order'] = 'asc'
    elif sort_option == 'price_desc':
        sort['key'] = 'price'
        sort['order'] = 'desc'
    elif sort_option == 'rating_asc':
        sort['key'] = 'rating'
        sort['order'] = 'asc'
    elif sort_option == 'rating_desc':
        sort['key'] = 'rating'
        sort['order'] = 'desc'   
    return sort



# def update_product(db, product:Product) -> True | str:
#     """
#     Returns [bool] True on success
#     Returns [str] error message on fail
#     """
#     ...