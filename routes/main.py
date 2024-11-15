from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash
from Models.user import User
from datetime import datetime, timedelta

main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db):

    @main.route('/')
    def index():
        return render_template('index.html')
    
    
    @main.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Get email and password from form
            user_login = request.form.get('email')
            password = request.form.get('password')
            
            # Find the user by email
            user = User.query.filter_by(email=user_login).first()

            # Check if user exists and password is correct
            if user:
                if user.blocked_until >= datetime.datetime.now():
                    flash(f'You are blocked until {user.blocked_until.strftime('%Y-%m-%d %H:%M')}.', 'danger')
                else:
                    if user.check_password(password):
                        login_user(user)
                        user.blocked_until = None
                        user.failed_count = 0
                        return redirect(url_for('index'))
                    user.failed_count += 1
                    if user.failed_count >= 4:
                        user.blocked_until == datetime.datetime.now() + timedelta(hours=1)
                    elif user.failed_count >= 3:
                        user.blocked_until >= datetime.datetime.now() + timedelta(minutes=5)
                    flash('Invalid email or password. Please try again.', 'danger')
            else:
                flash('Invalid email or password. Please try again.', 'danger')
                
        return render_template('login.html')
    

    @main.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user_first_name = request.form.get('name')
            user_last_name = request.form.get('surname')
            user_email = request.form.get('email-register')
            user_password = request.form.get('password-register')

            flash(f'TEST {user_first_name} {user_last_name} {user_email} {user_password} {user_password}.', 'info')
                
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
    
    # register blueprint

    app.register_blueprint(main)
