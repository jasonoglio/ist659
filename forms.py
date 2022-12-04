from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

from wtforms import BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')