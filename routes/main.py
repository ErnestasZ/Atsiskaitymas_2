from flask import Blueprint, render_template, request, flash, redirect, url_for
import Controllers.main_myaccount as myac
import Controllers.admin_order as ador
import Services.Forms.user_form as us_forms
import Services.Forms.dashboard as dash_forms
main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @main.route('/')
    def index():
        return render_template('index.html')

    @main.route('/login')
    def login():
        return render_template('login.html')

    @main.route('/logout')
    def logout():
        flash('You have been logged out.', 'main info')
        return redirect(url_for('main.index'))

    # @main.route('/lost-password', methods=['GET', 'POST'])
    # def lost_password():
    #     return render_template('lost_password.html')

    @main.route('/my-account')
    def my_acc():
        return render_template('my_account.html')

    @main.route('/my-account/orders')
    def my_orders():
        orders, total = myac.get_user_orders_by_id(5)  # pass user id
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
        user_id = 5  # pass user id
        balance = myac.get_user_balance(user_id)
        form = us_forms.BalanceForm()
        if form.validate_on_submit():
            myac.add_balance(user_id, form.balance.data)  # pass user id
            flash('Balance updated successfully.', 'main success')
            return redirect(url_for('main.my_balance'))
        return render_template('balance.html', balance=balance, form=form)

    @main.route('/my-account/user-details', methods=['GET', 'POST'])
    def my_details():
        user = myac.get_login_user(5)  # pass user id
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

    @main.route('/cart')
    def cart():
        return render_template('cart.html')

    @main.route('/checkout')
    def checkout():
        return render_template('checkout.html')

    # register blueprint

    app.register_blueprint(main)
