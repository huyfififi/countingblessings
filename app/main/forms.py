from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField(label='What is your name?', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class EditProfileForm(FlaskForm):
    name = StringField(label='Name(0~64 chars)', validators=[Length(0, 64)])
    about_me = TextAreaField(label='About me(0~1000 chars)',
                             validators=[Length(0, 1000)])
    submit = SubmitField(label='Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(),
                        Length(1, 64), Email()])
    username = StringField(label='Username(1~64 chars)', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField(label='Confirmed')
    role = SelectField(label='Role', coerce=int)
    name = StringField(label='Name(0~64 chars)', validators=[Length(0, 64)])
    about_me = TextAreaField(label='About me(0~1000 chars)',
                             validators=[Length(0, 1000)])
    submit = SubmitField(label='Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    body = TextAreaField(label='Did something good happen?',
                         validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(label='Submit')
