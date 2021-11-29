import jwt
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import requests
from flask import flash, redirect, url_for, Blueprint, render_template, request, session
from flask_mail import Message
from app.extensions import mail
from config import RESET_PASSWORD_MESSAGE, RESET_PASSWORD_WARNING, SECRET_KEY, URL
from app.views.forms import (RegistrationForm,
                             LoginForm,
                             RequestForm,
                             HandleRequestForm,
                             SearchRequestForm,
                             SearchEmployeeForm,
                             RequestResetForm,
                             ResetPasswordForm,
                             SearchDepartmentForm)

auth = Blueprint('auth', name)
general = Blueprint('general', name)


def validate_token():
    if 'token' not in session:
        return False
    try:
        jwt.decode(session['token'], SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        session.pop('token', None)
        session.pop('current_user_id', None)
        session.pop('department_id', None)
        session.pop('role_id', None)
        return False
    session['token'] = jwt.encode({'id': session['current_user_id'],
                                   'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                                  SECRET_KEY, algorithm='HS256')
    return True


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if validate_token():
        flash('You are already logged in', 'info')
        return redirect(url_for('general.departments_page'))
    form = RegistrationForm()
    response_deps = requests.get(f'{URL}/deps',
                                 json={'register': True})
    form.department.choices = [department['title'] for department in response_deps.json()['departments']]
    if form.validate_on_submit():
        response = requests.post(f'{URL}/api_register',
                                 json={'firstname': form.firstname.raw_data,
                                       'lastname': form.lastname.raw_data,
                                       'email': form.email.raw_data,
                                       'password': form.password.raw_data,
                                       'birth_date': form.birth_date.raw_data,
                                       'dep_title': form.department.raw_data})
        if response.status_code == 201:
            flash('Your account has been created!', 'success')
            return redirect(url_for('auth.login'))
        elif response.status_code == 400:
            flash(response.reason)
    return render_template('register.html', title='Registration Page', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if validate_token():
        flash('You are already logged in', 'info')
        return redirect(url_for('general.departments_page'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            if request.method == 'POST':
                email = form.email.data
                password = form.password.data
                response = requests.post(f'{URL}/api_login', json={'email': email,
                                                                   'password': password})
                session.permanent = True
                session['token'] = response.json()['token']
                session['current_user_id'] = response.json()['current_user_id']
                session['department_id'] = response.json()['department_id']
                session['role_id'] = response.json()['role_id']
                return redirect(url_for('general.departments_page'))
            else:
                flash('Login unsuccessful. There may be a typo.', 'danger')
        except ValueError:
            flash('Login unsuccessful. There may be a typo.', 'danger')
    return render_template('login.html', title='Login Page', form=form)


@auth.route('/logout')
def logout():
    if not validate_token():
        flash('You should be logged in to access this page', 'info')
        return redirect(url_for('auth.login'))
    session.pop('token', None)
    session.pop('current_user_id', None)
    session.pop('department_id', None)
    session.pop('role_id', None)
    return redirect(url_for('general.departments_page'))


@auth.route('/profile')
def profile():
    if not validate_token():
        flash('You need to be logged in to access this page', 'info')
        return redirect(url_for('auth.login'))
    response_emp = requests.get(f'{URL}/emp/{session["current_user_id"]}',
                                json={'token': session['token']})
    if response_emp.status_code != 200:
        flash('Something went wrong', 'danger')
        return redirect(url_for('general.departments_page'))
    response_dep = requests.get(f'{URL}/dep/{session["department_id"]}',
                                json={'token': session['token']})
    if response_dep.status_code != 200:
        flash('Something went wrong', 'danger')
        return redirect(url_for('general.departments_page'))
    return render_template('profile.html',
                           title='Profile Page',
                           employee=response_emp.json()['user'],
                           department=response_dep.json()['department'])


def send_reset_email(employee):
    token = get_reset_token(employee)
    msg = Message('Password Reset Request',
                  recipients=[employee['email']])
    msg.body = RESET_PASSWORD_MESSAGE + url_for('auth.reset_token', token=token,
                                                _external=True) + RESET_PASSWORD_WARNING
    mail.send(msg)


def get_reset_token(employee, expires_sec=1800):
    s = Serializer(SECRET_KEY, expires_sec)
    return s.dumps({'employee_id': employee['id']}).decode('utf-8')


def verify_reset_token(token):
    s = Serializer(SECRET_KEY)
    try:
        employee_id = s.loads(token)['employee_id']
    except:
        return None
    response_emp = requests.get(f'{URL}/emp/{employee_id}',
                                json={'token': session['token']})
    return response_emp.json()['user']


@auth.route('/reset-password', methods=['POST', 'GET'])
def reset_request():
    if validate_token():
        return redirect(url_for('general.departments_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        response = requests.get(f'{URL}/emp/{session["current_user"].id}',
                                json={'token': session['token']})
        employee = response.json()
        send_reset_email(employee)
        flash('An email with reset password instructions has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route('/reset-password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if validate_token():
        return redirect(url_for('general.departments_page'))
    employee = verify_reset_token(token)
    if employee is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        response = requests.patch(f'{URL}/emp/{employee["id"]}',
                                  json={'token': session['token'],
                                        'password': form.password.data})
        if response.status_code != 200:
            flash('Something went wrong', 'danger')
        else:
            flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Token', form=form)


@general.route('/', methods=['POST', 'GET'])
def departments_page():
    if not validate_token():
        return redirect(url_for('auth.login'))
    form = SearchDepartmentForm()
    departments = dict()
    if form.search.data:
        response = requests.get(f'{URL}/deps/search/{form.search.data}',
                                json={'token': session['token']})
        if response.status_code != 200:
            flash('Something went wrong', 'danger')
        else:
            departments = response.json()['departments']
    else:
        response = requests.get(f'{URL}/deps',
                                json={'token': session['token']})
        if response.status_code != 200:
            flash('Something went wrong', 'danger')
        else:
            departments = response.json()['departments']

    def avg(lst):
        if not lst:
            return 0
        else:
            return round(sum(lst) / len(lst), 2)

    deps = [[department, avg([employee['salary'] for employee in department['employees']])]
            for department in departments]
    return render_template('departments.html',
                           title='Departments Page',
                           form=form,
                           departments=deps)


@general.route('/department/<int:department_id>', methods=['POST', 'GET'])
def department_page(department_id):
    if not validate_token():
        flash('You need to be logged in to access this page', 'info')
        return redirect(url_for('auth.login'))
    response_dep = requests.get(f'{URL}/dep/{department_id}',
                                json={'token': session['token']})
    form = SearchEmployeeForm()
    if form.search.data:
        response_emps = requests.get(f'{URL}/emps/search/{form.search.data}',
                                     json={'token': session['token'],
                                           'filter': f'or_(Employee.firstname.contains("{form.search.data}"),'
                                                     f' Employee.lastname.contains("{form.search.data}")),'
                                                     f' Employee.department_id == {department_id}'})
        employees = response_emps.json()['users']
    else:
        employees = response_dep.json()['department']['employees']
    return render_template('department.html',
                           title=response_dep.json()['department']['title'],
                           employees=employees,
                           form=form)


@general.route('/employee/<int:employee_id>')
def employee_page(employee_id):
    if not validate_token():
        return redirect(url_for('auth.login'))
    if 'token' in session:
        if employee_id == session['current_user_id']:
            return redirect(url_for('auth.profile'))
    response_emp = requests.get(f'{URL}/emp/{employee_id}',
                                json={'token': session['token']})
    if response_emp.status_code != 200:
        flash('Something went wrong', 'danger')
        return redirect(url_for('general.departments_page'))
    response_dep = requests.get(f'{URL}/dep/{response_emp.json()["user"]["department_id"]}',
                                json={'token': session['token']})
    if response_dep.status_code != 200:
        flash('Something went wrong', 'danger')
        return redirect(url_for('general.departments_page'))
    return render_template('employee.html',
                           title=f'{response_emp.json()["user"]["firstname"]} {response_emp.json()["user"]["lastname"]}',
                           employee=response_emp.json()["user"],
                           department=response_dep.json()["department"])


@general.route('/about')
def about_page():
    return render_template('about.html', title='About Page')


@general.route('/send-request', methods=['POST', 'GET'])
def send_request():
    if not validate_token():
        flash('You need to be logged in to access this page', 'info')
        return redirect(url_for('auth.login'))
    if session['role_id'] == 4:
        flash('Only regular users can request changes.', 'warning')
        return redirect(url_for('general.departments_page'))
    form = RequestForm()
    response_deps = requests.get(f'{URL}/deps',
                                 json={'token': session['token']})
    #departments = [department for department in Department.query.all()]
    response_dep = requests.get(f'{URL}/dep/{session["department_id"]}',
                                json={'token': session['token']})
    departments = response_deps.json()['departments']
    department = response_dep.json()['department']
    #department_to_remove = Department.query.get(session['current_user']['department_id'])
    departments.remove(department)
    #departments.remove(department_to_remove)
    form.change_department.choices = [''] + [dep['title']
                                             for dep in departments]
    form.increase_salary.choices = [''] + ['1%', '5%', '10%', '20%']
    if form.validate_on_submit():
        if form.change_department.data or form.increase_salary.data:
            if form.change_department.data:
                response_change_dep = requests.get(f'{URL}/deps',
                                                   json={'token': session['token'],
                                                         'filter': f'title="{form.change_department.data}"'})
                #change_department = Department.query.filter_by(title=form.change_department.data).first()
                change_department = response_change_dep.json()['departments'][0]['id']
            else:
                change_department = 0
            if form.increase_salary.data:
                increase_salary = int(form.increase_salary.data[:-1])
            else:
                increase_salary = 0
            response_req = requests.post(f'{URL}/req',
                                         json={'token': session['token'],
                                               'sender': session['current_user_id'],
                                               'change_department_id': change_department,
                                               'increase_salary': increase_salary})
            if response_req.status_code != 200:
                flash('Something went wrong', 'danger')
                return redirect(url_for('general.departments_page'))
            flash('Your request has been sent!', 'success')
            return redirect(url_for('general.departments_page'))
        else:
            flash('You need to request at least one change to send the request!', 'warning')
    return render_template('request_form.html', title='Send Request Page', form=form)


@general.route('/requests', methods=['POST', 'GET'])
def requests_page():
    """
    if current_user.role_id != 4:
        flash('Permission to access this page denied. This is an admin-only page.', 'danger')
        return redirect(url_for('general.departments_page'))
    """
    if not validate_token():
        flash('You need to be logged in to access this page', 'info')
        return redirect(url_for('auth.login'))
    form = SearchRequestForm()
    if form.search.data:
        if session['role_id'] == 4:
            response_reqs = requests.get(f'{URL}/reqs',
                                         json={'token': session['token'],
                                               'filter': f'or_(Employee.firstname.contains("{form.search.data}"),'
                                                         f' Employee.lastname.contains("{form.search.data}")),'
                                                         f' Request.status == 0,'
                                                         f' Employee.id == Request.sender'})


        else:
            response_reqs = requests.get(f'{URL}/reqs',
                                         json={'token': session['token'],
                                               'filter': f'or_(Employee.firstname.contains("{form.search.data}"),'
                                                         f' Employee.lastname.contains("{form.search.data}")),'
                                                         f' {session["current_user_id"]} == Request.sender,'
                                                         f' Employee.id == {session["current_user_id"]}'})
    else:
        if session['role_id'] == 4:
            response_reqs = requests.get(f'{URL}/reqs',
                                         json={'token': session['token'],
                                               'filter': f'Request.status == 0,'
                                                         f'Employee.id == Request.sender'})
        else:
            response_reqs = requests.get(f'{URL}/reqs',
                                         json={'token': session['token'],
                                               'filter': f'{session["current_user_id"]} == Request.sender,'
                                                         f'Employee.id == {session["current_user_id"]}'})
    requests_list = response_reqs.json()['reqs'][::-1]
    return render_template('requests.html',
                           title='Requests Page',
                           form=form,
                           requests=requests_list)


@general.route('/request/<int:request_id>', methods=['POST', 'GET'])
def request_page(request_id):
    if not validate_token():
        flash('You need to be logged in to access this page', 'info')
        return redirect(url_for('auth.login'))
    response_req = requests.get(f'{URL}/req/{request_id}',
                                json={'token': session['token']})
    if response_req.status_code != 200:
        flash('Something went wrong', 'danger')
        return redirect(url_for('general.departments_page'))
    req = response_req.json()['req']
    if req['sender'] != session['current_user_id'] and session['role_id'] != 4:
        flash('Access to this page is denied for unauthorized users!', 'danger')
        return redirect(url_for('general.requests_page'))
    response_emp = requests.get(f'{URL}/emp/{req["sender"]}',
                                json={'token': session['token']})
    if response_emp.status_code != 200:
        flash('Something went wrong', 'danger')
        return redirect(url_for('general.departments_page'))
    sender = response_emp.json()['user']
    if req['change_department_id']:
        response_dep = requests.get(f'{URL}/dep/{req["change_department_id"]}')
        if response_dep.status_code != 200:
            flash('Something went wrong', 'danger')
            return redirect(url_for('general.departments_page'))
        change_department = response_dep.json()['department']
    else:
        change_department = None
    form = None
    if session['role_id'] == 4:# and request.status == 0:
        form = HandleRequestForm()
        if form.validate_on_submit():
            #Check in case where different admins process the same request
            if req['status'] != 0:
                flash('This request was already processed!', 'warning')
                return redirect(url_for('general.requests_page'))
            if form.accept.data:
                if req['change_department_id']:
                    response_patch_emp = requests.patch(f'{URL}/emp/{req["sender"]}',
                                                        json={'token': session['token'],
                                                              'department_id': req['change_department_id']})
                    if response_patch_emp.status_code != 200:
                        flash('Something went wrong', 'danger')
                        return redirect(url_for('general.departments_page'))
                if req['increase_salary']:
                    response_patch_emp = requests.patch(f'{URL}/emp/{req["sender"]}',
                                                        json={'token': session['token'],
                                                              'salary': round(sender['salary']
                                                                              + sender['salary']
                                                                              * (req['increase_salary'] / 100), 2)})
                    if response_patch_emp.status_code != 200:
                        flash('Something went wrong', 'danger')
                        return redirect(url_for('general.departments_page'))
                response_patch_req = requests.patch(f'{URL}/req/{req["id"]}',
                                                    json={'token': session['token'],
                                                          'status': 1})
                if response_patch_req.status_code != 200:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('general.departments_page'))
            else:
                response_patch_req = requests.patch(f'{URL}/req/{req["id"]}',
                                                    json={'token': session['token'],
                                                          'status': 2})
                if response_patch_req.status_code != 200:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('general.departments_page'))
            return redirect(url_for('general.requests_page'))
    return render_template('request.html',
                           title='Request Page',
                           request=req,
                           sender=sender,
                           form=form,
                           change_department=change_department)
