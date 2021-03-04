from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(),
                        Length(1, 64), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Keep me logged in')
    submit = SubmitField(label='Log In')


class RegistrationForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(),
                        Length(1, 64), Email()])
    username = StringField(label='Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField(label='Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField(label='Confirm password',
                              validators=[DataRequired()])
    submit = SubmitField(label='Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(label='Old password',
                                 validators=[DataRequired()])
    password = PasswordField(label='New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField(label='Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField(label='Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(),
                        Length(1, 64), Email()])
    submit = SubmitField(label='Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField(label='New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField(label='Confirm password',
                              validators=[DataRequired()])
    submit = SubmitField(label='Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField(label='New Email', validators=[DataRequired(),
                        Length(1, 64), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
