from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from Models import User, Loyalty
from Services.admin_forms import UserView, LoyaltyView
# from Services.forms import testas
admin = Blueprint('admin_panel', __name__, url_prefix='/admin')


def register_admin_routes(app, db):


    flask_admin = Admin(app, name="Admin Dashboard", template_mode="bootstrap2", base_template="admin/my_master.html")
    flask_admin.add_view(UserView(User, db.session))
    flask_admin.add_view(LoyaltyView(Loyalty, db.session))

    @admin.route('/')
    def index():
        return render_template('admin/index.html')

    # register blueprint
    app.register_blueprint(admin)
