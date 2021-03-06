import requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.models import Employee
from config import URL


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(max=20)])
    birth_date = DateField('Date Of Birth',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    department = SelectField('Department', choices=[],
                             validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        "the function validates the email submitted by the user in the registration form"
        #employee = Employee.query.filter_by(email=email.data).first()
        response = requests.get(f'{URL}/emp/{email.data}',
                                json={'token': ''})
        if response.status_code == 200:
            "if the user with such email already exists, an error occurs"
            raise ValidationError('The user with this email already exists. Try to log in.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        "the function validates the email submitted by the user in the reset-password form"
        #employee = Employee.query.filter_by(email=email.data).first()
        response = requests.get(f'{URL}/emp/{email.data}',
                                json={'token': ''})
        if response.status_code != 200:
            "if the user with such email doesn't exist, an error occurs"
            raise ValidationError('There is no account with such email. There may be a typo.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class SearchDepartmentForm(FlaskForm):
    search = StringField()
    submit = SubmitField('Search')


class SearchEmployeeForm(FlaskForm):
    search = StringField()
    submit = SubmitField('Search')


class RequestForm(FlaskForm):
    change_department = SelectField('Change My Department To', choices=[], default=[''])
    increase_salary = SelectField('Increase My Salary By', choices=[], default=[''])
    submit = SubmitField('Send Request')


class SearchRequestForm(FlaskForm):
    search = StringField()
    submit = SubmitField('Search')


class HandleRequestForm(FlaskForm):
    accept = SubmitField('Accept')
    decline = SubmitField('Decline')
