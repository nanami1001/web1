from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '請先登入才能使用評價功能'
login_manager.login_message_category = 'info'

def create_app(config_name=None, config_class=None):
    """Application factory. Pass either `config_class` or `config_name`.

    `config_name` can be one of: 'development', 'production', 'testing'. If
    neither is provided, `DevelopmentConfig` is used when FLASK_ENV is 'development',
    otherwise ProductionConfig.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Resolve configuration class
    if config_class is None:
        from project.config import DevelopmentConfig, ProductionConfig, TestingConfig
        env = config_name or os.environ.get('FLASK_ENV') or os.environ.get('APP_ENV')
        if env == 'testing':
            config_class = TestingConfig
        elif env == 'development' or env == 'dev':
            config_class = DevelopmentConfig
        else:
            config_class = ProductionConfig

    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    from project.routes.auth import auth
    from project.routes.main import main
    from project.routes.account import account_bp
    from project.routes.posts import posts_bp
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(account_bp)
    app.register_blueprint(posts_bp)

    with app.app_context():
        db.create_all()

    return app
