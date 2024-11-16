from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash
from Models.user import User
from Models.product import Product
from datetime import datetime, timedelta
from Controllers.user import create_user, get_user_by_email, update_user
from Controllers.product import get_average_rating, get_reviews, get_products

main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db):
    @main.route('/')
    def index():
        sort_option = request.args.get('sort_option', 'default') # Default to 'default'
        sort = {'key': 'default', 'order': 'asc'}  # Default sorting by title (asc)
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

        products = get_products(db, {sort['key']: sort['order']})
        for product in products:
            product.average_rating = get_average_rating(product)
        return render_template('index.html', products=products, sort_option=sort_option)

    @main.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        average_rating = get_average_rating(product)
        reviews = get_reviews(product)
        return render_template('product.html', product=product, average_rating=average_rating, reviews=reviews)

    
    @main.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Get email and password from form
            user_login = request.form.get('email')
            password = request.form.get('password')
            # Find the user by email
            user = get_user_by_email(db, user_login)
            # Check if user exists and password is correct
            if user and not user.is_deleted:
                if user.blocked_until >= datetime.datetime.now():
                    flash(f'You are blocked until {user.blocked_until.strftime('%Y-%m-%d %H:%M')}.', 'danger')
                else:
                    if user.check_password(password):
                        login_user(user)
                        user.blocked_until = None
                        user.failed_count = 0
                        update_user(db, user)
                        return redirect(url_for('index'))
                    user.failed_count += 1
                    if user.failed_count >= 4:
                        user.blocked_until == datetime.datetime.now() + timedelta(hours=1)
                    elif user.failed_count >= 3:
                        user.blocked_until >= datetime.datetime.now() + timedelta(minutes=5)
                    update_user(db, user)
                    flash('Invalid email or password. Please try again.', 'danger')
            else:
                flash('Invalid email or password. Please try again.', 'danger')
        return render_template('login.html')
    

    @main.route('/register', methods=['GET', 'POST'])
    def register():
        return render_template('login.html')
    

    @main.route('/logout')
    def logout():
        flash('You have been logged out.', 'info')
        return redirect(url_for('main.index'))
    
    # @main.route('/lost-password', methods=['GET', 'POST'])
    # def lost_password():
    #     return render_template('lost_password.html')
    
    @main.route('/my-account')
    def my_acc():
        return render_template('my_account.html')
    
    @main.route('/cart')
    def cart():
        return render_template('cart.html')
    
    @main.route('/checkout')
    def checkout():
        return render_template('checkout.html')
    
    @main.route('/product-search')
    def product_search():
        return render_template('search.html')
    
    # register blueprint

    app.register_blueprint(main)
