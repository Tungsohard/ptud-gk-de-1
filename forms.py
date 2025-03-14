from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Ghi nhớ đăng nhập')  # Thêm trường này
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    image = FileField('Hình ảnh', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Đăng bài')

class CommentForm(FlaskForm):
    content = TextAreaField('Nội dung bình luận', validators=[DataRequired()])
    submit = SubmitField('Đăng bình luận')