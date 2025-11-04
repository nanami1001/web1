from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '請先登入才能使用評價功能'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    from project.config import Config
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
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
