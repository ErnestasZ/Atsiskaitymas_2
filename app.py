from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Misc.my_logger import my_logger

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
    app.config['SECRET_KEY'] = 'your_secret_key'

    # mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Your email address
    app.config['MAIL_PASSWORD'] = 'your-email-password'  # Your email password (or app password for Gmail)
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@gmail.com'  # Default sender email

    db.init_app(app)

    my_logger.info('app created')

    # register Models
    import Models

    # register new routes from routes folder
    from routes.main import register_main_routes
    from routes.admin import register_admin_routes
    register_main_routes(app, db)
    register_admin_routes(app, db)

    migrate = Migrate(app, db)

    return app
