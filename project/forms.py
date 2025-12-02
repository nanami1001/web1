from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email, ValidationError
from wtforms import validators
from project.models import User

class RegisterForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('電子郵件', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('密碼', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('註冊')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('該使用者名稱已被使用')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('該電子郵件已被註冊')

class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    submit = SubmitField('登入')

class RatingForm(FlaskForm):
    score = IntegerField('評分 (1~5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('留言')
    submit = SubmitField('送出評價')


class TwoFactorForm(FlaskForm):
    token = StringField('驗證碼', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('驗證')

class UpdateAccountForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('電子郵件', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('更新資料')
    picture = FileField('更新頭像', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])


class PostForm(FlaskForm):
    title = StringField('標題', validators=[DataRequired(), Length(max=140)])
    content = TextAreaField('內容', validators=[DataRequired()])
    picture = FileField('貼文圖片', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('發布')


class RequestResetForm(FlaskForm):
    email = StringField('電子郵件', validators=[DataRequired(), Email()])
    submit = SubmitField('寄出密碼重設信')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError('沒有這個電子郵件的帳號，請先註冊')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('密碼', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重設密碼')
