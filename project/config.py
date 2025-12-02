import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 新增上傳圖片相關設定
    UPLOAD_FOLDER = os.path.join('project', 'static', 'profile_pics')
    POST_UPLOAD_FOLDER = os.path.join('project', 'static', 'post_pics')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Email settings for password reset
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') in ['True', 'true', '1']
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    # default sender for outgoing mail — fallback to MAIL_USERNAME if not set
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('EMAIL_USER'))
    # (No debug link exposure — always return safe failure states)