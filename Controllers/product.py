from sqlalchemy import select, not_, and_, or_
from Models import Product, Review, Order_item
from Controllers import db_provider as dbp

session = dbp.db.session

def get_product_by_id(id: int) -> (Product | None):
    stmt = select(Product).where(Product.id == id)
    return session.execute(stmt).scalars().first()

def get_all_products() -> list[Product]:
    return session.execute(select(Product)).scalars().all()

def update_product(id: int = None, product: Product = None, **kwargs) -> (Product | Exception):
    if not product and id:
        product = get_product_by_id(id)
    
    if isinstance(product, Product):
        result = dbp.push_db_record(product, **kwargs)
    else:
        result = ValueError("Unable to update a non-existent database record!")
    return result

def add_product(**kwargs) -> (Product | Exception):
    return dbp.push_db_record(Product, **kwargs)

def get_average_rating(product):
    total_rating = sum(review.rating for order_item in product.order_items for review in order_item.reviews if review.rating is not None)
    total_reviews = sum(1 for order_item in product.order_items for review in order_item.reviews if review.rating is not None)
    if total_reviews > 0:
        average_rating = total_rating / total_reviews
        return round(average_rating, 1)  
    return None

def get_reviews(product):
    reviews = []
    for order_item in product.order_items:
        reviews.extend(order_item.reviews)
    return reviews


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

    if name:
        query = query.filter(Product.title.ilike(f"%{name}%"))
    
    if price:
        min_price, max_price = price
        query = query.filter(Product.price >= min_price, Product.price <= max_price)
    
    if sort:
        for key, direction in sort.items():
            if key == 'default':
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

    for product in products:
        product.average_rating = get_average_rating(product)

    if 'rating' in sort:
        products.sort(key=lambda p: (p.average_rating is not None, p.average_rating), reverse=(sort['rating'].lower() == 'desc'))

    return products