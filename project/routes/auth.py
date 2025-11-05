
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from project import db, bcrypt
from project.models import User
from flask_login import login_user, logout_user, current_user
from flask_login import login_required
from project.forms import RegisterForm, LoginForm, TwoFactorForm
import pyotp
import qrcode
import io
import base64

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()

    if form.validate_on_submit():  # ✅ 這一層非常重要
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            image_file='default.jpg'  # 確保新用戶有預設頭像
        )
        db.session.add(user)
        db.session.commit()
        flash("註冊成功！請登入", "success")
        return redirect(url_for('auth.login'))

    return render_template("register.html", form=form)  # 這行縮排要與 if 同層

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # If user has 2FA enabled, start pre-2FA flow
            if getattr(user, 'two_factor_enabled', False):
                session['pre_2fa_user_id'] = user.id
                # preserve next page across 2FA
                session['pre_2fa_next'] = request.args.get('next')
                return redirect(url_for('auth.two_factor'))

            login_user(user)
            flash("登入成功！", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        else:
            flash("帳號或密碼錯誤", "danger")
    return render_template("login.html", form=form)

@auth.route("/logout")
def logout():
    flash("您已登出", "info")
    logout_user()
    return redirect(url_for('main.home'))


@auth.route('/two_factor', methods=['GET', 'POST'])
def two_factor():
    """Verify TOTP during login (pre-login flow)."""
    user_id = session.get('pre_2fa_user_id')
    if not user_id:
        flash('未找到待驗證的使用者，請重新登入', 'warning')
        return redirect(url_for('auth.login'))

    form = TwoFactorForm()
    if form.validate_on_submit():
        user = User.query.get(user_id)
        if user and user.two_factor_secret:
            totp = pyotp.TOTP(user.two_factor_secret)
            if totp.verify(form.token.data):
                login_user(user)
                session.pop('pre_2fa_user_id', None)
                next_page = session.pop('pre_2fa_next', None)
                flash('登入成功（步驟 2）', 'success')
                return redirect(next_page or url_for('main.home'))
        flash('驗證碼錯誤或已過期', 'danger')

    return render_template('two_factor.html', form=form)


@auth.route('/two_factor/setup', methods=['GET', 'POST'])
@login_required
def two_factor_setup():
    """Setup 2FA: generate secret, show QR and confirm token to enable."""
    if getattr(current_user, 'two_factor_enabled', False):
        flash('你已啟用二次驗證', 'info')
        return redirect(url_for('main.home'))

    # generate or reuse temporary secret in session
    if 'two_factor_secret_setup' not in session:
        session['two_factor_secret_setup'] = pyotp.random_base32()
    secret = session['two_factor_secret_setup']

    # otpauth url for authenticator apps
    label = current_user.email if getattr(current_user, 'email', None) else current_user.username
    otpauth_url = pyotp.TOTP(secret).provisioning_uri(name=label, issuer_name="新光三越台南小北門店")

    # generate QR as base64 PNG
    img = qrcode.make(otpauth_url)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_b64 = base64.b64encode(buffered.getvalue()).decode()

    form = TwoFactorForm()
    if form.validate_on_submit():
        totp = pyotp.TOTP(secret)
        if totp.verify(form.token.data):
            current_user.two_factor_secret = secret
            current_user.two_factor_enabled = True
            db.session.commit()
            session.pop('two_factor_secret_setup', None)
            flash('二次驗證已啟用', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('驗證碼錯誤，請重試', 'danger')

    return render_template('two_factor_setup.html', form=form, qr_b64=qr_b64, secret=secret)
