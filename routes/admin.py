from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from Models.user import User
# from Services.forms import testas
admin = Blueprint('admin_pane', __name__, url_prefix='/admin_panel')


def register_admin_routes(app, db):
    adminF = Admin(app, name='Admin Panel', template_mode='bootstrap3')

    @admin.route('/')
    def index():
        return render_template('admin/indexes.html')

    adminF.add_view(ModelView(User, db.session))
    # register blueprint
    app.register_blueprint(admin)
