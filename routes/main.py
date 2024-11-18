from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from Models.user import User
from datetime import datetime, timedelta
from flask_login import LoginManager
from Controllers.user import create_user, get_user_by_email, update_user

main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db):

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @main.route('/')
    def index():
        return render_template('index.html')
    
    
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
                if user.veryfied_at is None:
                    # [!] pakartotinai issiusti verifikavimo e-mail
                    flash(f'Your e-mail is not verified. Check your e-mail anf follow the link.', 'warning')
                elif (not user.blocked_until is None) and (user.blocked_until >= datetime.now()):
                    flash(f'You are blocked until {user.blocked_until.strftime('%Y-%m-%d %H:%M')}.', 'danger')
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
                flash('Email is already registered. Please use a different email.', 'danger')
                return redirect(url_for('main.login'))
            # create
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                token='',  # You may want to set a token for email verification
                veryfied_at=datetime.now(),  # You can make this False until email is verified
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
                # Log the user in immediately after registration
                login_user(new_user)
                flash('Your account has been created successfully!', 'success')
                return redirect(url_for('main.index'))
        return redirect(url_for('main.login'))
    

    @main.route('/logout')
    def logout():
        logout_user()
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
