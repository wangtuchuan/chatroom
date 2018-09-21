from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    website = StringField('Website', validators=[Optional(), URL(), Length(0, 128)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(0, 120)])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

