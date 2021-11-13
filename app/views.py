from flask import flash, redirect, url_for, Blueprint, render_template, request
from flask_wtf import FlaskForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.extensions import db, bcr, login_manager
from app.models import Department, Employee, Role


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


auth = Blueprint('auth', __name__)
general = Blueprint('general', __name__)


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
        employee = Employee.query.filter_by(email=email.data).first()
        if employee:
            raise ValidationError('The user with this email already exists. Try to log in.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    search = StringField()
    submit = SubmitField('Search')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('general.departments_page'))
    form = RegistrationForm()
    form.department.choices = [department.title for department in Department.query.all()]
    if form.validate_on_submit():
        hashed_password = bcr.generate_password_hash(form.password.data).decode('utf-8')
        dep = Department.query.filter_by(title=form.department.data).first()
        role = Role.query.filter_by(name='regular').first()
        employee = Employee(firstname=form.firstname.data,
                            lastname=form.lastname.data,
                            birth_date=form.birth_date.data,
                            email=form.email.data,
                            password=hashed_password,
                            department_id=dep.id,
                            role_id=role.id)
        db.session.add(employee)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Registration Page', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('general.departments_page'))
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee and bcr.check_password_hash(employee.password, form.password.data):
            login_user(employee, remember=form.remember.data)
            return redirect(url_for('general.departments_page'))
        else:
            flash('Login unsuccessful. There may be a typo.', 'danger')
    return render_template('login.html', title='Login Page', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('general.departments_page'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile Page')


@general.route('/', methods=['POST', 'GET'])
def departments_page():
    form = SearchForm()
    if form.search.data:
        departments = Department.query.filter(Department.title.contains(form.search.data)).all()
    else:
        departments = Department.query.all()
    return render_template('departments.html', title='Departments Page', form=form, departments=departments)


@general.route('/department/<int:department_id>')
def department_page(department_id):
    department = Department.query.get(department_id)
    return render_template('department.html', title=department.title, employees=department.employees)


@general.route('/employee/<int:employee_id>')
def employee_page(employee_id):
    if employee_id == current_user.id:
        return redirect(url_for('auth.profile'))
    employee = Employee.query.get(employee_id)
    return render_template('employee.html', title=f'{employee.firstname} {employee.lastname}', employee=employee)


@general.route('/about')
def about_page():
    return render_template('about.html', title='About Page')
