from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.secret_key = 'SOME_SECRET_KEY'

    db.init_app(app)

    # register Models
    import Models

    # register new routes from routes folder
    from routes.main import register_main_routes
    from routes.admin import register_admin_routes
    register_main_routes(app, db)
    register_admin_routes(app, db)

    migrate = Migrate(app, db)

    return app
