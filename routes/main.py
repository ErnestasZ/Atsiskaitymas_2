from flask import Blueprint, render_template, request, flash, redirect, url_for
main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db):

    @main.route('/')
    def index():
        return render_template('index.html')
    
    @main.route('/login')
    def login():
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
    
    @main.route('/my-account/orders')
    def my_orders():
        return render_template('orders.html')
    
    @main.route('/my-account/balance')
    def my_balance():
        return render_template('balance.html')
    
    @main.route('/my-account/user-details')
    def my_details():
        return render_template('user_details.html')
    
    @main.route('/cart')
    def cart():
        return render_template('cart.html')
    
    @main.route('/checkout')
    def checkout():
        return render_template('checkout.html')
    
    # register blueprint

    app.register_blueprint(main)
