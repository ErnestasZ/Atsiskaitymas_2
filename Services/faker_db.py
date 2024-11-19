from Models import User, Product, Order, Wallet_transaction, Order_item, Review
from Controllers.user import create_user

from app import db, create_app
from faker import Faker
from datetime import datetime, timedelta
import random


fake = Faker()


def get_random_date_within_week():
    now = datetime.now()
    weeks_ago = now - timedelta(weeks=16)
    random_date = weeks_ago + (now - weeks_ago) * random.random()
    return random_date


def get_image_link_from_txt():
    with open("Misc/links.txt", "r") as file:
        images = file.read().splitlines()
    return images


image_link_list = get_image_link_from_txt()
password = 'secret123'


def populate_db():
    admin = User.query.filter_by(email="admin@admin.com").first()
    if not admin:
        admin = User(
            first_name="Admin",
            last_name="",
            email="admin@admin.com",
            is_deleted=False,
            verified_at = datetime.now(),
            is_admin=True,
            failed_count=0
        )
        admin.set_password('123')
        create_user(db, admin)
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    for _ in range(10):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            is_deleted=False,
            verified_at = datetime.now(),
            is_admin=False,
            failed_count=0
        )
        user.set_password(user.first_name[:3])
        db.session.add(user)

    for _ in range(30):
        product = Product(
            title=fake.word().capitalize(),
            image=random.choice(image_link_list),
            description=fake.text(),
            price=round(random.uniform(10, 100), 2),
            stock=random.randint(1, 100)
        )
        db.session.add(product)

    db.session.commit()

    user_ids = [user.id for user in User.query.all()]
    product_ids = [product.id for product in Product.query.all()]
    products = {product.id: product for product in Product.query.all()}

    for _ in range(10):
        created_at = get_random_date_within_week()
        order = Order(
            user_id=random.choice(user_ids),
            status="Pending",
            total_amount=0,
            created_at=created_at
        )
        db.session.add(order)
        db.session.flush()

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
                product_name=product.title,
                unit_price=unit_price,
                total_price=total_price,
                created_at=created_at
            )
            db.session.add(order_item)
            db.session.flush()

            review = Review(
                order_item_id=order_item.id,
                content=fake.text(),
                rating=random.randint(1, 5)
            )
            db.session.add(review)
            order_total += total_price

        order.total_amount = order_total

    for user_id in user_ids:
        for _ in range(random.randint(1, 5)):
            transaction = Wallet_transaction(
                user_id=user_id,
                amount=round(random.uniform(20, 1000), 2)
            )
            db.session.add(transaction)

    db.session.commit()
    print("Database populated successfully.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_db()

# populate_db()
