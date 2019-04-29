from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import Client


class RegistrationForm(FlaskForm):
    def validate_client_name(self, field):
        if Client.query.filter_by(client_name=field.data).first():
            raise ValidationError('Username already taken')

    client_name = StringField('Username:', validators=[
        DataRequired(),
        validate_client_name
    ])
    password = PasswordField('Password:',
                             validators=[DataRequired()
                                         ])
    password2 = PasswordField("Confirm Password:", validators=[DataRequired()])
    submit = SubmitField('Register User')


class LoginForm(FlaskForm):
    client_name = StringField('Username:', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
