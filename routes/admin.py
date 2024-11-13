from flask import render_template, request, flash, redirect, url_for

def register_admin_routes(app, db):

    @app.route('/admin')
    def admin_index():
        return render_template('admin/index.html')