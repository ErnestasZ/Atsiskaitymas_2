from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, g
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from Models.user import User
from datetime import datetime, timedelta

from Models import *
from Controllers import *
# All imports are implemented here, no need to import a specific function!
# Add module imports similar to the above.

# from Models.user import User
# from Models.product import Product
# from Controllers.user import create_user, get_user_by_email, update_user
# from Controllers.product import get_average_rating, get_reviews, get_products

import Controllers.main_myaccount as myac
import Controllers.admin_order as ador
import Services.Forms.user_form as us_forms
import Services.Forms.dashboard as dash_forms
from flask_login import LoginManager
from Controllers.user import create_user, get_user_by_email, update_user, verify_user_token
from flask_mail import Mail
from Services.mail import send_verification_email

main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    login_manager = LoginManager()
    login_manager.init_app(app)

    mail = Mail(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @main.route('/')
    def index():
        search_option = request.args.get('search', '').strip()
        min_price = request.args.get('min_price', None)  # Get min price
        max_price = request.args.get('max_price', None)  # Get max price
        sort_option = request.args.get(
            'sort_option', 'default')  # Default to 'default'

        sort = get_sorting_option(sort_option)  # Sorting options

        products = get_products(
            db, {sort['key']: sort['order']}, name=search_option, price=[min_price, max_price])

        for product in products:
            product.average_rating = get_average_rating(
                product)  # Get rating for each product in list

        no_products_message = None
        if not products:
            no_products_message = "No products found."

        return render_template('index.html', products=products, sort_option=sort_option, name=search_option, min_price=min_price, max_price=max_price, no_products_message=no_products_message)

    @main.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)  # get products by ID
        average_rating = get_average_rating(product)  # get product rating
        reviews = get_reviews(product)  # get product revievs
        return render_template('product.html', product=product, average_rating=average_rating, reviews=reviews)

    @main.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        if request.method == 'POST':
            # Get email and password from form
            user_login = request.form.get('login_email')
            password = request.form.get('login_password')
            # Find the user by email
            user = get_user_by_email(db, user_login)
            # Check if user exists and password is correct
            if user and not user.is_deleted:
                if not (user.blocked_until is None) and user.blocked_until >= datetime.now():
                    flash(f'You are blocked until {
                          user.blocked_until.strftime('%Y-%m-%d %H:%M')}.', 'danger')
                if user.verified_at is None:
                    # [!] pakartotinai issiusti verifikavimo e-mail
                    flash(
                        f'Your e-mail is not verified. Check your e-mail anf follow the link.', 'warning')
                elif (not user.blocked_until is None) and (user.blocked_until >= datetime.now()):
                    flash(f'You are blocked until {
                          user.blocked_until.strftime('%Y-%m-%d %H:%M')}.', 'danger')
                else:
                    if user.check_password(password):
                        login_user(user)
                        user.blocked_until = None
                        user.failed_count = 0
                        update_user(db, user)
                        return redirect(url_for('main.index'))
                    user.failed_count += 1
                    if user.failed_count >= 4:
                        user.blocked_until == datetime.now() + timedelta(hours=1)
                    elif user.failed_count >= 3:
                        user.blocked_until >= datetime.now() + timedelta(minutes=5)
                    update_user(db, user)
                    flash('Invalid email or password. Please try again.', 'danger')
            else:
                flash('Invalid email or password. Please try again.', 'danger')
        return render_template('login.html')

    @main.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            # Get user input from the registration form
            first_name = request.form['register_first_name']
            last_name = request.form['register_last_name']
            email = request.form['register_email']
            password = request.form['register_password']
            confirm_password = request.form['register_confirm_password']
            # validations
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('main.login'))
            existing_user = get_user_by_email(db, email)
            if existing_user:
                flash(
                    'Email is already registered. Please use a different email.', 'danger')
                return redirect(url_for('main.login'))
            # create
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                token='',  # You may want to set a token for email verification
                verified_at=None,
                is_admin=False,
                is_deleted=False,
                blocked_until=None,
                failed_count=0,
                loyalty_id=None
            )
            new_user.set_password(password)
            result = create_user(db, new_user)
            if result is not True:
                flash(result, 'danger')
                return redirect(url_for('main.login'))
            else:
                # send user verification email
                send_verification_email(mail, new_user)
                flash('Your account has been created successfully!', 'success')
                return redirect(url_for('main.registration_success'))
        return redirect(url_for('main.login'))
    

    @main.route('/registration_success', methods=['GET', 'POST'])
    def registration_success():
        return render_template('registration_success.html')


    @main.route('/logout')
    def logout():
        flash('You have been logged out.', 'main info')
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('main.index'))


    @app.route('/verify-email/<token>')
    def verify_email(token):
        r = verify_user_token(db, token)
        if r is True:
            flash('Your email has been verified!', 'success')
            return redirect(url_for('main.login'))
        else:
            flash(r, 'danger')
            return redirect(url_for('main.index'))

    # @main.route('/lost-password', methods=['GET', 'POST'])
    # def lost_password():
    #     return render_template('lost_password.html')

    @main.route('/my-account')
    def my_acc():
        return render_template('my_account.html')

    @main.route('/my-account/orders')
    def my_orders():
        orders, total = myac.get_user_orders_by_id(3)  # pass user id
        return render_template('orders.html', orders=orders, total=total)

    @main.route('/my-account/orders/<int:order_id>')
    def my_order_items(order_id):
        items, order, _status = ador.get_order_items(order_id)
        return render_template('order_items.html', order=order, items=items)

    @main.route('/my-account/orders/<int:order_id>/<int:item_id>', methods=['POST', 'GET'])
    def my_item_review(order_id, item_id):
        review, order = ador.get_item_review(item_id)
        form = dash_forms.ReviewForm(
            rating=review.rating,
            content=review.content
        )
        if form.validate_on_submit():
            ador.set_review(item_id, form.rating.data, form.content.data)
            flash('Review updated successfully.', 'main success')
            return redirect(url_for('main.my_item_review', order_id=order_id, item_id=item_id))
        # if form.validate_on_submit():
        #     ador.set_order_status(order_id, form.status.data)
        #     flash('Review added successfully.', 'success')
        #     return redirect(url_for('main.my_order_items', order_id=order_id, item_id=item_id))

        return render_template('item_review.html',
                               review=review,
                               order=order,
                               form=form)

    @main.route('/<int:order_id>/review/<int:item_id>/delete/<int:review_id>', methods=['POST'])
    def my_delete_review(order_id, item_id, review_id):
        ador.remove_review(review_id)
        flash('Review deleted successfully.', 'admin success')
        return redirect(url_for('main.my_item_review', order_id=order_id, item_id=item_id))

    @main.route('/my-account/balance', methods=['GET', 'POST'])
    def my_balance():
        user_id = 3  # pass user id
        balance = myac.get_user_balance(user_id)
        form = us_forms.BalanceForm()
        if form.validate_on_submit():
            myac.add_balance(user_id, form.balance.data)  # pass user id
            flash('Balance updated successfully.', 'main success')
            return redirect(url_for('main.my_balance'))
        return render_template('balance.html', balance=balance, form=form)

    @main.route('/my-account/user-details', methods=['GET', 'POST'])
    def my_details():
        user = myac.get_login_user(3)  # pass user id
        user_form = us_forms.UserForm(
            # email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        if 'user_form_submit' in request.form and user_form.validate_on_submit():
            myac.edit_user(user.id, user_form)
            flash('User details updated successfully', 'main success')
            return redirect(url_for('main.my_details'))

        return render_template('user_details.html',
                               user=user,
                               user_form=user_form
                               )

        # return render_template('user_details.html')

    @main.route('/add_to_cart/<int:product_id>', methods=['POST'])
    def add_to_cart(product_id):
        qty = request.form.get('qty', 1)  # Default quantity
        session_id = get_session_id()  # Get fake session ID

        # Check if product already in the cart
        cart_product = Cart_product.query.filter_by(
            session_id=session_id, product_id=product_id).first()

        if cart_product:
            cart_product.qty += int(qty)
        else:
            cart_product = Cart_product(
                session_id=session_id, product_id=product_id, qty=int(qty))
            db.session.add(cart_product)

        db.session.commit()
        return jsonify({'message': 'Product added to cart'})

    @main.route('/cart')
    def cart():
        session_id = get_session_id()
        cart_products = Cart_product.query.filter_by(
            session_id=session_id).all()
        total_price = sum(item.product.price *
                          item.qty for item in cart_products)
        total_price = round(total_price, 2)
        return render_template('cart.html', cart_products=cart_products, total_price=total_price)

    @main.route('/update_cart', methods=['POST'])
    def update_cart():
        session_id = get_session_id()  # Get session ID

        # all form fields
        for key, value in request.form.items():
            if key.startswith('qty_'):
                # Extract item ID from the form field name
                item_id = int(key.split('_')[1])
                cart_item = Cart_product.query.get(item_id)
                if cart_item:
                    cart_item.qty = int(value)  # Update the quantity
            elif key.startswith('remove_'):
                item_id = int(key.split('_')[1])  # Extract item ID for removal
                cart_item = Cart_product.query.get(item_id)
                if cart_item:
                    db.session.delete(cart_item)  # Remove item
        db.session.commit()
        return redirect(url_for('main.cart'))

    @main.before_app_request
    def before_request():
        session_id = get_session_id()
        g.cart_quantity = db.session.query(db.func.sum(Cart_product.qty)).filter_by(
            session_id=session_id).scalar() or 0

    @main.route('/checkout')
    def checkout():
        return render_template('checkout.html')

    # register blueprint

    app.register_blueprint(main)
