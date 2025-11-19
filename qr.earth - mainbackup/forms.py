from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField
from wtforms.validators import InputRequired, Email, Optional

class PersonalDetailsForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired(message="Full Name is required")])
    company_name = StringField('Company Name', validators=[Optional()])  # Optional field
    email_address = EmailField('Email Address', validators=[InputRequired(message="Email is required"), Email()])
    mobile_number = TelField('Mobile Number', validators=[InputRequired(message="Mobile Number is required")])
    address = StringField('Address', validators=[Optional()])  # Optional field
    linkedin_profile = StringField('LinkedIn Profile', validators=[Optional()])  # Optional field
    instagram = StringField('Instagram', validators=[Optional()])  # Optional field
    facebook = StringField('Facebook', validators=[Optional()])
    submit = SubmitField('Finish and Download QR Code')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from models import User

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

from wtforms import PasswordField

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')