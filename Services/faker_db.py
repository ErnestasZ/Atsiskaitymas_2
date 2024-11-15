from Models import User, Product, Order, Wallet_transaction, Order_item, Review

from app import db, create_app
from faker import Faker
import random


fake = Faker()


def populate_db():
    # Create 1 admin user
    admin = User.query.filter_by(email="admin@admin.com").first()
    if not admin:
        # Create 1 admin user if not already present
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@admin.com",
            password="secret123",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    # Create 10 regular users
    for _ in range(10):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            password=fake.password(),
            is_admin=False
        )
        db.session.add(user)

    # Create 30 products
    for _ in range(30):
        product = Product(
            title=fake.word().capitalize(),
            description=fake.text(),
            price=round(random.uniform(10, 100), 2),
            stock=random.randint(1, 100)
        )
        db.session.add(product)

    # Commit the users and products first to set up relationships
    db.session.commit()

    # Create 10 orders, each assigned to a random user and containing random order items
    user_ids = [user.id for user in User.query.all()]
    product_ids = [product.id for product in Product.query.all()]
    # Preload product details for efficient lookup
    products = {product.id: product for product in Product.query.all()}

    for _ in range(10):
        # Create an order associated with a random user
        order = Order(
            user_id=random.choice(user_ids),
            status="Pending",  # Example status
            total_amount=0  # Will be calculated based on order items
        )
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID for the relationship with order items

        # Create 1–5 random order items for this order
        order_total = 0
        for _ in range(random.randint(1, 5)):
            product_id = random.choice(product_ids)
            product = products[product_id]
            qty = random.randint(1, 5)
            unit_price = product.price
            total_price = qty * unit_price
            order_item = Order_item(
                order_id=order.id,
                product_id=product_id,
                qty=qty,
                product_name=product.title,  # Assuming `title` is the product name
                unit_price=unit_price,
                total_price=total_price
            )
            db.session.add(order_item)
            db.session.flush()

            review = Review(
                order_item_id=order_item.id,
                content=fake.text(),  # Generate random review content
                rating=random.randint(1, 5)  # Rating between 1 and 5
            )
            db.session.add(review)
            order_total += total_price

        # Update the total amount for the order
        order.total_amount = order_total

    # Create wallet transactions for each user
    for user_id in user_ids:
        for _ in range(random.randint(1, 5)):  # Each user has between 1 and 5 transactions
            transaction = Wallet_transaction(
                user_id=user_id,
                amount=round(random.uniform(20, 1000), 2)
            )
            db.session.add(transaction)

    # Commit all remaining data
    db.session.commit()
    print("Database populated successfully.")


if __name__ == "__main__":
    app = create_app()  # Create the app instance
    with app.app_context():  # Run within the app context
        populate_db()

# populate_db()
