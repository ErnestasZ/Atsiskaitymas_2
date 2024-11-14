from flask import Blueprint, render_template, request, flash, redirect, url_for
# from Services.forms import testas
admin = Blueprint('admin', __name__, url_prefix='/admin')


def register_admin_routes(app, db):

    @admin.route('/')
    def index():
        return render_template('admin/index.html')

    # register blueprint
    app.register_blueprint(admin)
