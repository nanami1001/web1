from flask import Blueprint, render_template, url_for, flash, request, redirect
from flask_login import login_required, current_user
from project import db
from project.forms import UpdateAccountForm
from project.utils import save_picture, allowed_file
from werkzeug.utils import secure_filename

account_bp = Blueprint('account', __name__)

@account_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # 不直接用 secure_filename 去改變原始檔名，改由 save_picture 內部判斷副檔名並產生安全檔名
            filename = form.picture.data.filename
            if allowed_file(filename):
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            else:
                flash('不支援的檔案格式。請使用 PNG、JPG、JPEG 或 GIF 檔案。', 'danger')
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('您的帳戶資料已更新！', 'success')
        return redirect(url_for('account.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + (current_user.image_file or 'default.jpg'))
    return render_template('account.html', title='帳戶管理',
                           image_file=image_file, form=form)