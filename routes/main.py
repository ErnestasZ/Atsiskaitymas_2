from flask import Blueprint, render_template, request, flash, redirect, url_for
main = Blueprint('main', __name__, url_prefix='/')


def register_main_routes(app, db):

    @main.route('/')
    def index():
        return render_template('index.html')

    # register blueprint
    app.register_blueprint(main)
