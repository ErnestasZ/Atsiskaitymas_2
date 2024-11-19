from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, g
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
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
# from flask_mail import Mail
from Services.mail import send_verification_email

main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db:SQLAlchemy):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    # mail = Mail(app)

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
        
        loyalty_discount = get_loyalty_discount()

        for product in products:
            product.average_rating = get_average_rating(product)  # Get rating for each product in list
            
            # Apply loyalty discount to product price
            if loyalty_discount > 0:
                product.discounted_price = product.price * (1 - loyalty_discount / 100)
            else:
                product.discounted_price = product.price

        no_products_message = None
        if not products:
            no_products_message = "No products found."

        return render_template('index.html', products=products, sort_option=sort_option, name=search_option, min_price=min_price, max_price=max_price, no_products_message=no_products_message)

    @main.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)  # get products by ID
        average_rating = get_average_rating(product)  # get product rating
        reviews = get_reviews(product)  # get product revievs
        loyalty_discount = get_loyalty_discount()

        if loyalty_discount > 0:
            discounted_price = product.price * (1 - loyalty_discount / 100)
        else:
            discounted_price = product.price
        return render_template('product.html', product=product, average_rating=average_rating, reviews=reviews, discounted_price=discounted_price)

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
                    # pakartotinai issiunciam verifikavimo e-mail
                    send_verification_email(user)
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
                send_verification_email(new_user)
                flash('Your account has been created successfully!', 'success')
                return redirect(url_for('main.registration_success'))
        return redirect(url_for('main.login'))

    @main.route('/registration_success', methods=['GET', 'POST'])
    def registration_success():
        return render_template('registration_success.html')

    @main.route('/logout')
    def logout():
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
    @login_required
    def my_acc():
        
        return render_template('my_account.html')

    @main.route('/my-account/orders')
    @login_required
    def my_orders():
        orders, total = myac.get_user_orders_by_id(
            current_user.id)  # pass user id
        return render_template('orders.html', orders=orders, total=total)

    @main.route('/my-account/orders/<int:order_id>')
    @login_required
    def my_order_items(order_id):
        items, order, _status = ador.get_order_items(order_id)
        return render_template('order_items.html', order=order, items=items)

    @main.route('/my-account/orders/<int:order_id>/<int:item_id>', methods=['POST', 'GET'])
    @login_required
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
    @login_required
    def my_balance():
        # user_id = current_user.id
        # balance = myac.get_user_balance(user_id)
        balance = current_user.get_balance()
        form = us_forms.BalanceForm()
        if form.validate_on_submit():
            # pass user id
            myac.add_balance(current_user.id, form.balance.data)
            flash('Balance updated successfully.', 'main success')
            return redirect(url_for('main.my_balance'))
        return render_template('balance.html', balance=balance, form=form)

    @main.route('/my-account/user-details', methods=['GET', 'POST'])
    @login_required
    def my_details():
        user = myac.get_login_user(current_user.id)  # pass user id
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
        try:
            qty = int(request.form.get('qty', 1)) # Default quantity if not passed
        except:
            flash('Quantity must be number', 'error')
            return redirect(request.referrer)
        
        session_id = get_session_id()
        product = get_product_by_id(product_id)
        if not product:
            flash('Product you are trying to add is not available.', 'warning')
            return redirect(request.referrer)
        
        if current_user.is_authenticated:
            user_id = current_user.id
            cart_product = get_cart_product(db, session_id=None, product_id=product_id, user_id=user_id)
        else:
            user_id = None
            cart_product = get_cart_product(db, session_id=session_id, product_id=product_id)

        
        if cart_product:
            qty = cart_product.qty + int(qty)
            if qty > product.stock:
                qty = product.stock
            cart_product.qty = qty
            db.session.commit()
            flash('Product you are trying to add is not available.', 'warning')
        else:
            if qty > product.stock:
                qty = product.stock
            new_cart_product = Cart_product(session_id=session_id, user_id=user_id, product_id=product_id, qty=qty)
            if add_cart_product(db, new_cart_product):
                flash('Product added to cart.', 'success')
            else:
                flash('Error occured while adding product. Please contact administrator.', 'warning')
        return redirect(request.referrer)
        

    @main.route('/cart')
    def cart():
        if current_user.is_authenticated:
            cart_products = get_cart(db, None, user_id=current_user.id)
        else:
            session_id = get_session_id()
            cart_products = get_cart(db, session_id)

        total_price = sum(item.product.price * item.qty for item in cart_products)
        total_price = round(total_price, 2)
        loyalty_discount = get_loyalty_discount()
        return render_template('cart.html', cart_products=cart_products, total_price=total_price, loyalty_discount=loyalty_discount)

    @main.route('/remove_cart_item/<int:product_id>', methods=['GET'])
    def remove_cart_item(product_id):
        session_id = get_session_id()  # Get session ID
            
        if current_user.is_authenticated:
            user_id = current_user.id
            cart_product = get_cart_product(db, session_id=None, product_id=product_id, user_id=user_id)
        else:
            user_id = None
            cart_product = get_cart_product(db, session_id=session_id, product_id=product_id)
            
        if not cart_product:
            print('qwdas')
            flash(f'Product you are trying to remove is not in your cart', 'warning')
            return redirect(url_for('main.cart'))


        print(cart_product)             
        flash(f'Product {cart_product.product.title} was removed from your cart', 'success')
        db.session.delete(cart_product)
        db.session.commit()
        return redirect(url_for('main.cart'))
    
    @main.route('/update_cart', methods=['POST'])
    def update_cart():
        session_id = get_session_id()  # Get session ID
        for key, qty in request.form.items():
            try:
                qty = int(qty)
            except:
                flash('Quantity must be number', 'error')
                return redirect(request.referrer)

            if qty < 1:
                flash('Quantity must be 1 or higher', 'error')
                return redirect(request.referrer)
            
            product_id = int(key.split('_')[1])
            product = get_product_by_id(product_id)
            if current_user.is_authenticated:
                user_id = current_user.id
                cart_product = get_cart_product(db, session_id=None, product_id=product_id, user_id=user_id)
            else:
                user_id = None
                cart_product = get_cart_product(db, session_id=session_id, product_id=product_id)
            
            if not product:
                flash(f'Product {cart_product.product.title} is no longer available and was removed from your cart', 'warning')
                db.session.delete(cart_product)
                db.session.commit
                continue

            if key.startswith('productid_'):
                # Extract item ID from the form field name
                if cart_product:
                    if qty > product.stock:
                        qty = product.stock
                        flash(f'We do not have enough product {cart_product.product.title} in stock quantity was automatically updated to {qty}', 'warning')
                    if cart_product.qty != qty:
                        cart_product.qty = qty
                        db.session.commit()
                        flash(f'Product {cart_product.product.title} quantity was updated successfully to {qty}', 'warning')
        return redirect(url_for('main.cart'))

    @main.before_app_request
    def before_request():
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            user_id = None
        session_id = get_session_id()
        g.cart_quantity = len(get_cart(db, session_id, user_id))

    @main.route('/checkout')
    @login_required
    def checkout():
        session_id = get_session_id()
        cart_products = Cart_product.query.filter_by(session_id=session_id).all()

        if cart_products:
            fill_user(cart_products, current_user)
            discount = get_loyalty_discount()
            order = Order(user_id=current_user.id, status="Pending", loyalty_discount=discount)
            db.session.add(order)
            msg = ""
            
            total_amount = 0
            for item in cart_products:
                if item.qty > item.product.stock:
                    msg = "Prekių kiekis viršija kiekį esanti sandėlyje"
                
                unit_price = item.product.price * (1 - discount / 100)
                total_price = unit_price * item.qty
                order_item = Order_item(order_id=order.id,
                                        product_id=item.product.id,
                                        qty=item.qty,
                                        product_name=item.product.title,
                                        unit_price=unit_price,
                                        total_price=total_price)
                total_amount += total_price
                db.session.add(order_item)
                db.session.delete(item)

            if total_amount > current_user.get_balance():
                msg = "Neužtenka lėšų apmokėjimui!"

            if not msg:
                try:
                    order.total_amount = total_amount
                    db.session.add(order)
                    db.session.Commit()
                    msg = "Orderis sukurtas sekmingai"
                except Exception as err:
                    msg = err
                else:
                    return render_template('order_items.html', order=order, items=order.order_items)
        else:
            msg = "Krepšelyje nėra prekių!"
        return render_template('checkout.html', msg)

    # register blueprint

    app.register_blueprint(main)
