from flask import flash, redirect, url_for, Blueprint, render_template
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from app.extensions import db, bcr, login_manager, mail
from app.models.models import Department, Employee, Role, Request
from config import RESET_PASSWORD_MESSAGE, RESET_PASSWORD_WARNING
from sqlalchemy import or_
from app.views.forms import (RegistrationForm,
                             LoginForm,
                             RequestForm,
                             HandleRequestForm,
                             SearchRequestForm,
                             SearchEmployeeForm,
                             RequestResetForm,
                             ResetPasswordForm,
                             SearchDepartmentForm)


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


auth = Blueprint('auth', __name__)
general = Blueprint('general', __name__)


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
                            role_id=role.id,
                            salary=0)
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('general.departments_page'))


@auth.route('/profile')
@login_required
def profile():
    department = Department.query.get(current_user.department_id)
    return render_template('profile.html',
                           title='Profile Page',
                           department=department)


def send_reset_email(employee):
    token = employee.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[employee.email])
    msg.body = RESET_PASSWORD_MESSAGE + url_for('auth.reset_token', token=token,
                                                _external=True) + RESET_PASSWORD_WARNING
    mail.send(msg)


@auth.route('/reset-password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('general.departments_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        send_reset_email(employee)
        flash('An email with reset password instructions has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route('/reset-password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('general.departments_page'))
    employee = Employee.verify_reset_token(token)
    if employee is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcr.generate_password_hash(form.password.data).decode('utf-8')
        employee.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Token', form=form)


@general.route('/', methods=['POST', 'GET'])
def departments_page():
    form = SearchDepartmentForm()
    if form.search.data:
        departments = Department.query.filter(Department.title.contains(form.search.data)).all()
    else:
        departments = Department.query.all()

    def avg(lst):
        if not lst:
            return 0
        else:
            return round(sum(lst) / len(lst), 2)

    departments = [[department, avg([employee.salary for employee in department.employees])]
                   for department in departments]
    return render_template('departments.html',
                           title='Departments Page',
                           form=form,
                           departments=departments)


@general.route('/department/<int:department_id>', methods=['POST', 'GET'])
def department_page(department_id):
    department = Department.query.get(department_id)
    form = SearchEmployeeForm()
    if form.search.data:
        employees = Employee.query.filter(or_(Employee.firstname.contains(form.search.data),
                                          Employee.lastname.contains(form.search.data)),
                                          Employee.department_id == department_id).all()
    else:
        employees = department.employees
    return render_template('department.html', title=department.title, employees=employees, form=form)


@general.route('/employee/<int:employee_id>')
def employee_page(employee_id):
    if current_user.__class__.__name__ != 'AnonymousUserMixin':
        if employee_id == current_user.id:
            return redirect(url_for('auth.profile'))
    employee = Employee.query.get(employee_id)
    department = Department.query.get(employee.department_id)
    return render_template('employee.html',
                           title=f'{employee.firstname} {employee.lastname}',
                           employee=employee,
                           department=department)


@general.route('/about')
def about_page():
    return render_template('about.html', title='About Page')


@general.route('/send-request', methods=['POST', 'GET'])
@login_required
def send_request():
    if current_user.role_id == 4:
        flash('Only regular users can request changes.', 'warning')
        return redirect(url_for('general.departments_page'))
    form = RequestForm()
    departments = [department for department in Department.query.all()]
    department_to_remove = Department.query.get(current_user.department_id)
    departments.remove(department_to_remove)
    form.change_department.choices = [''] + [department.title for department in departments]
    form.increase_salary.choices = [''] + ['1%', '5%', '10%', '20%']
    if form.validate_on_submit():
        if form.change_department.data or form.increase_salary.data:
            if form.change_department.data:
                change_department = Department.query.filter_by(title=form.change_department.data).first()
                change_department = change_department.id
            else:
                change_department = 0
            if form.increase_salary.data:
                increase_salary = int(form.increase_salary.data[:-1])
            else:
                increase_salary = 0
            req = Request(sender=current_user.id,
                          change_department_id=change_department,
                          increase_salary=increase_salary,
                          status=0)
            db.session.add(req)
            db.session.commit()
            flash('Your request has been sent!', 'success')
            return redirect(url_for('general.departments_page'))
        else:
            flash('You need to request at least one change to send the request!', 'warning')
    return render_template('request_form.html', title='Send Request Page', form=form)


@general.route('/requests', methods=['POST', 'GET'])
@login_required
def requests_page():
    """
    if current_user.role_id != 4:
        flash('Permission to access this page denied. This is an admin-only page.', 'danger')
        return redirect(url_for('general.departments_page'))
    """
    form = SearchRequestForm()
    if form.search.data:
        if current_user.role_id == 4:
            requests_list = db.session.query(Request, Employee).filter(or_(Employee.firstname.contains(form.search.data),
                                                                           Employee.lastname.contains(form.search.data)),
                                                                       Request.status == 0,
                                                                       Employee.id == Request.sender).all()
        else:
            requests_list = db.session.query(Request, Employee).filter(
                or_(Employee.firstname.contains(form.search.data),
                    Employee.lastname.contains(form.search.data)),
                Request.status == 1 or Request.status == 2,
                Employee.id == current_user.id).all()
    else:
        if current_user.role_id == 4:
            requests_list = db.session.query(Request, Employee).filter(Request.status == 0,
                                                                       Employee.id == Request.sender).all()
        else:
            requests_list = db.session.query(Request, Employee).filter(Employee.id == current_user.id,
                                                                       current_user.id == Request.sender).all()
    requests_list = requests_list[::-1]
    return render_template('requests.html',
                           title='Requests Page',
                           form=form,
                           requests=requests_list)


@general.route('/request/<int:request_id>', methods=['POST', 'GET'])
@login_required
def request_page(request_id):
    request = Request.query.get(request_id)
    if not request:
        flash('This request does not exist!', 'danger')
        return redirect(url_for('general.requests_page'))
    elif request.sender != current_user.id and current_user.role_id != 4:
        flash('Access to this page is denied for unauthorized users!', 'danger')
        return redirect(url_for('general.requests_page'))
    sender = Employee.query.get(request.sender)
    if request.change_department_id:
        change_department = Department.query.get(request.change_department_id)
    else:
        change_department = None
    form = None
    if current_user.role_id == 4:# and request.status == 0:
        form = HandleRequestForm()
        if form.validate_on_submit():
            #Check in case where different admins process the same request
            if request.status != 0:
                flash('This request was already processed!', 'warning')
                return redirect(url_for('general.requests_page'))
            if form.accept.data:
                if request.change_department_id:
                    Employee.query.filter_by(id=request.sender).update({'department_id'
                                                                        : request.change_department_id})
                if request.increase_salary:
                    Employee.query.filter_by(id=request.sender).update({'salary'
                                                                        : round(sender.salary
                                                                          + sender.salary
                                                                          * (request.increase_salary / 100), 2)})
                Request.query.filter_by(id=request.id).update({'status'
                                                               : 1})
            else:
                Request.query.filter_by(id=request.id).update({'status'
                                                               : 2})
            db.session.commit()
            return redirect(url_for('general.requests_page'))
    return render_template('request.html',
                           title='Request Page',
                           request=request,
                           sender=sender,
                           form=form,
                           change_department=change_department)