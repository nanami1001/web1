import os
import secrets
from PIL import Image
from flask import current_app


def _extension_from_filename_or_image(form_picture):
    """Return a dot-prefixed extension (e.g. .jpg) determined from filename or image data."""
    # Try from filename first
    filename = getattr(form_picture, 'filename', '') or ''
    _, f_ext = os.path.splitext(filename)
    f_ext = f_ext.lower()
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    if f_ext and f_ext.lstrip('.') in allowed:
        return f_ext

    # Fallback: probe image data with PIL
    try:
        form_picture.stream.seek(0)
    except Exception:
        pass
    try:
        img = Image.open(form_picture)
        fmt = (img.format or '').lower()
        img.close()
        if fmt == 'jpeg':
            return '.jpg'
        if fmt:
            return f'.{fmt}'
    except Exception:
        pass

    # As last resort, default to .jpg
    return '.jpg'


def save_picture(form_picture):
    """Save avatar/profile picture to static/profile_pics and return generated filename."""
    random_hex = secrets.token_hex(8)
    f_ext = _extension_from_filename_or_image(form_picture)
    picture_fn = random_hex + f_ext

    folder = os.path.join(current_app.root_path, 'static', 'profile_pics')
    os.makedirs(folder, exist_ok=True)
    picture_path = os.path.join(folder, picture_fn)

    # 調整圖片大小
    output_size = (150, 150)
    try:
        form_picture.stream.seek(0)
    except Exception:
        pass
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # save using original format if available
    save_kwargs = {}
    if i.format:
        save_kwargs['format'] = i.format
    i.save(picture_path, **save_kwargs)
    i.close()

    return picture_fn


def save_post_picture(form_picture):
    """Save an uploaded picture for a post into static/post_pics and return filename."""
    random_hex = secrets.token_hex(8)
    f_ext = _extension_from_filename_or_image(form_picture)
    picture_fn = random_hex + f_ext

    post_folder = os.path.join(current_app.root_path, 'static', 'post_pics')
    # ensure folder exists
    os.makedirs(post_folder, exist_ok=True)

    picture_path = os.path.join(post_folder, picture_fn)

    # Resize posts images to reasonable size (max 800x800)
    output_size = (800, 800)
    try:
        form_picture.stream.seek(0)
    except Exception:
        pass
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    save_kwargs = {}
    if i.format:
        save_kwargs['format'] = i.format
    i.save(picture_path, **save_kwargs)
    i.close()

    return picture_fn