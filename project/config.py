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