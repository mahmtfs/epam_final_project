from flask import Blueprint, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


auth = Blueprint('auth', __name__)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                        validators=[DataRequired(), Length(max=20)])
    lastname = StringField('Last Name',
                        validators=[DataRequired(), Length(max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('general.departments_page'))
    return render_template('register.html', title='Registraion Page', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'a@gmail.com' and form.password.data == 'abc':
            flash('You have been logged in!', 'success')
            return redirect(url_for('general.departments_page'))
        else:
            flash('Login unsuccessful. There may be a typo.', 'danger')
    return render_template('login.html', title='Login Page', form=form)