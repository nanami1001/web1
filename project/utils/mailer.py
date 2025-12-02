from flask import current_app, render_template, url_for
from flask_mail import Message
from project import mail


def send_reset_email(user, token=None):
    """Send password reset email for user.

    Returns True on success, False on failure. On failure the caller should show
    a short generic error message and not expose tokens or debug links.
    """
    if token is None:
        token = user.get_reset_token()

    # build reset link (try _external; fallback to build with SERVER_NAME or localhost)
    try:
        link = url_for('auth.reset_token', token=token, _external=True)
    except RuntimeError:
        # try a non-external path; if that also fails (no request + no SERVER_NAME),
        # fallback to a simple path and prepend a sensible host
        try:
            path = url_for('auth.reset_token', token=token, _external=False)
        except RuntimeError:
            path = f"/reset_password/{token}"
        host = current_app.config.get('SERVER_NAME') or 'localhost:5000'
        scheme = current_app.config.get('PREFERRED_URL_SCHEME') or 'http'
        link = f"{scheme}://{host}{path}"

    # render bodies
    text_body = render_template('email/reset_password.txt', user=user, link=link)
    html_body = render_template('email/reset_password.html', user=user, link=link)

    sender = current_app.config.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_USERNAME')
    msg = Message('Password Reset Request', sender=sender, recipients=[user.email])
    msg.body = text_body
    msg.html = html_body

    try:
        mail.send(msg)
        return True
    except Exception:
        current_app.logger.exception('Failed to send reset email')
        return False
