from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Misc.my_logger import my_logger

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    my_logger.info('app created')

    # register Models
    import Models

    # register new routes from routes folder
    from routes.main import register_main_routes
    from routes.admin import register_admin_routes
    from routes.dashboard import register_dashboard_routes
    from routes.admin_order import register_order_routes
    from routes.payment import register_payment_routes
    register_main_routes(app, db)
    register_admin_routes(app, db)
    register_dashboard_routes(app, db)
    register_order_routes(app, db)
    register_payment_routes(app, db)

    migrate = Migrate(app, db)

    return app
