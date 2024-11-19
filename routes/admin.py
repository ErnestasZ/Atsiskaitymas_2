from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_admin import Admin
from Models import User, Loyalty, Wallet_transaction, Product, Order, Review
from Services.flask_admin_views import UserView, LoyaltyView, WalletView, ProductView, OrderModelView, ReviewModel
from flask_login import current_user


admin = Blueprint('admin_panel', __name__, url_prefix='/admin')


def register_admin_routes(app, db):

    flask_admin = Admin(app, name="Admin Dashboard", template_mode="bootstrap2", base_template="admin/my_master.html")

    
    flask_admin.add_view(UserView(User, db.session))
    flask_admin.add_view(LoyaltyView(Loyalty, db.session))
    flask_admin.add_view(WalletView(Wallet_transaction, db.session))
    flask_admin.add_view(ProductView(Product, db.session))
    flask_admin.add_view(OrderModelView(Order, db.session))
    flask_admin.add_view(ReviewModel(Review, db.session))

    @admin.route('/')
    def index():
        return render_template('admin/indexes.html')

    # register blueprint
    app.register_blueprint(admin)

    # @flask_admin.before_request
    # def restrict_to_admin():
    #     if not current_user or not current_user.is_admin:
    #         flash("Turi buti adminas")
    #         return redirect('/')
