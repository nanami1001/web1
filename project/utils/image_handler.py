import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    # 生成隨機檔名以避免衝突
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # 調整圖片大小
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # 保存圖片
    i.save(picture_path)
    
    return picture_fn


def save_post_picture(form_picture):
    """Save an uploaded picture for a post into static/post_pics and return filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    post_folder = os.path.join(current_app.root_path, 'static', 'post_pics')
    # ensure folder exists
    if not os.path.exists(post_folder):
        os.makedirs(post_folder, exist_ok=True)

    picture_path = os.path.join(post_folder, picture_fn)

    # Resize posts images to reasonable size (max 800x800)
    output_size = (800, 800)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn