from flask import render_template, request, flash, redirect, url_for


def register_main_routes(app, db):

    @app.route('/')
    def index():
        return render_template('index.html')
