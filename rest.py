import jwt
import datetime
from flask import request, jsonify, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from app import app
from app import db
from sqlalchemy import or_
from app.models.models import (Employee,
                               Department,
                               Request)


def validate_token(token):
    if not token:
        return make_response('there is no token', 400)
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return make_response('token invalid', 401)
    return make_response('token is valid', 200)


@app.route('/emps', methods=['GET'])
def get_all_employees():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)

    employees = Employee.query.all()
    output = []

    for emp in employees:
        emp_data = dict()
        emp_data['id'] = emp.id
        emp_data['firstname'] = emp.firstname
        emp_data['lastname'] = emp.lastname
        emp_data['email'] = emp.email
        emp_data['birth_date'] = emp.birth_date
        emp_data['department_id'] = emp.department_id
        emp_data['salary'] = emp.salary
        emp_data['role_id'] = emp.role_id
        output.append(emp_data)
    return jsonify({'users': output})


@app.route('/emp/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    if request.json['token']:
        valid = validate_token(request.json['token'])
        if valid.status_code != 200:
            return make_response(valid.response, valid.status_code)

    emp = Employee.query.get(emp_id)

    if not emp:
        return make_response('Employee not found', 404)

    emp_data = dict()
    emp_data['id'] = emp.id
    emp_data['firstname'] = emp.firstname
    emp_data['lastname'] = emp.lastname
    emp_data['email'] = emp.email
    emp_data['birth_date'] = emp.birth_date
    emp_data['department_id'] = emp.department_id
    emp_data['salary'] = emp.salary
    emp_data['role_id'] = emp.role_id
    emp_data['password'] = emp.password

    return jsonify({'user': emp_data})


@app.route('/emp/<email>', methods=['GET'])
def get_employee_email(email):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    if request.json['token']:
        valid = validate_token(request.json['token'])
        if valid.status_code != 200:
            return make_response(valid.response, valid.status_code)
    emp = Employee.query.filter_by(email=email).first()

    if not emp:
        return make_response('Employee not found', 404)

    emp_data = dict()
    emp_data['id'] = emp.id
    emp_data['firstname'] = emp.firstname
    emp_data['lastname'] = emp.lastname
    emp_data['email'] = emp.email
    emp_data['birth_date'] = emp.birth_date
    emp_data['department_id'] = emp.department_id
    emp_data['salary'] = emp.salary
    emp_data['role_id'] = emp.role_id
    emp_data['password'] = emp.password

    return jsonify({'user': emp_data})


@app.route('/emp', methods=['POST'])
def create_employee():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'])
    emps = Employee.query.all()
    ids = [emp.id for emp in emps]
    emp_id = max(ids) + 1
    new_emp = Employee(id=emp_id,
                       firstname=data['firstname'],
                       lastname=data['lastname'],
                       email=data['email'],
                       password=hashed_password,
                       birth_date=data['birth_date'],
                       department_id=data['department_id'],
                       role_id=3,
                       salary=0)
    db.session.add(new_emp)
    db.session.commit()
    return jsonify({'message': 'new employee created'})


@app.route('/emp/<int:emp_id>', methods=['PATCH'])
def patch_employee(emp_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    if request.json['token']:
        valid = validate_token(request.json['token'])
        if valid.status_code != 200:
            return make_response(valid.response, valid.status_code)
    emp = Employee.query.get(emp_id)

    if not emp:
        return make_response('Employee not found', 404)

    data = request.get_json()
    if 'password' in data:
        emp.password = generate_password_hash(data['password']).decode('ascii')
    if 'department_id' in data:
        emp.department_id = data['department_id']
    if 'salary' in data:
        emp.salary = data['salary']
    db.session.commit()
    return jsonify({'message': 'Employee updated'})


@app.route('/emp/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    emp = Employee.query.get(emp_id)

    if not emp:
        return make_response('Employee not found', 404)

    db.session.delete(emp)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'})


@app.route('/emps/search/<que>', methods=['GET'])
def search_emps(que):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    if 'filter' in request.json:
        fil = request.json['filter']
    else:
        return make_response('Insufficient data in request', 400)
    emps = eval(f'Employee.query.filter({fil}).all()')
    output = []
    for emp in emps:
        emp_data = dict()
        emp_data['id'] = emp.id
        emp_data['firstname'] = emp.firstname
        emp_data['lastname'] = emp.lastname
        emp_data['email'] = emp.email
        emp_data['birth_date'] = emp.birth_date
        emp_data['department_id'] = emp.department_id
        emp_data['salary'] = emp.salary
        emp_data['role_id'] = emp.role_id
        output.append(emp_data)
    return jsonify({'users': output})


@app.route('/deps', methods=['GET'])
def get_all_departments():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        if 'register' not in request.json:
            return make_response('Bad request', 400)
    else:
        valid = validate_token(request.json['token'])
        if valid.status_code != 200:
            return make_response(valid.response, valid.status_code)
    if 'filter' in request.json:
        departments = eval(f'Department.query.filter_by({request.json["filter"]}).first()')
    else:
        departments = Department.query.all()
    output = []
    if isinstance(departments, Department):
        dep_data = dict()
        dep_data['id'] = departments.id
        dep_data['title'] = departments.title
        dep_data['employees'] = []
        for emp in departments.employees:
            emp_data = dict()
            emp_data['id'] = emp.id
            emp_data['firstname'] = emp.firstname
            emp_data['lastname'] = emp.lastname
            emp_data['email'] = emp.email
            emp_data['birth_date'] = emp.birth_date
            emp_data['department_id'] = emp.department_id
            emp_data['salary'] = emp.salary
            emp_data['role_id'] = emp.role_id
            dep_data['employees'].append(emp_data)
        output.append(dep_data)
    else:
        for dep in departments:
            dep_data = dict()
            dep_data['id'] = dep.id
            dep_data['title'] = dep.title
            dep_data['employees'] = []
            for emp in dep.employees:
                emp_data = dict()
                emp_data['id'] = emp.id
                emp_data['firstname'] = emp.firstname
                emp_data['lastname'] = emp.lastname
                emp_data['email'] = emp.email
                emp_data['birth_date'] = emp.birth_date
                emp_data['department_id'] = emp.department_id
                emp_data['salary'] = emp.salary
                emp_data['role_id'] = emp.role_id
                dep_data['employees'].append(emp_data)
            output.append(dep_data)
    return jsonify({'departments': output})


@app.route('/dep/<int:dep_id>', methods=['GET'])
def get_department(dep_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)

    dep = Department.query.get(dep_id)

    if not dep:
        return make_response('Department not found', 404)

    dep_data = dict()
    dep_data['id'] = dep.id
    dep_data['title'] = dep.title
    dep_data['salary'] = dep.salary
    dep_data['employees'] = []
    for emp in dep.employees:
        emp_data = dict()
        emp_data['id'] = emp.id
        emp_data['firstname'] = emp.firstname
        emp_data['lastname'] = emp.lastname
        emp_data['email'] = emp.email
        emp_data['birth_date'] = emp.birth_date
        emp_data['department_id'] = emp.department_id
        emp_data['salary'] = emp.salary
        emp_data['role_id'] = emp.role_id
        dep_data['employees'].append(emp_data)
    return jsonify({'department': dep_data})


@app.route('/dep/<title>', methods=['GET'])
def get_department_title(title):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    if request.json['token']:
        valid = validate_token(request.json['token'])
        if valid.status_code != 200:
            return make_response(valid.response, valid.status_code)
    dep = Department.query.filter_by(title=title).first()

    if not dep:
        return make_response('Department not found', 404)

    dep_data = dict()
    dep_data['id'] = dep.id
    dep_data['title'] = dep.title
    dep_data['salary'] = dep.salary
    dep_data['employees'] = []
    for emp in dep.employees:
        emp_data = dict()
        emp_data['id'] = emp.id
        emp_data['firstname'] = emp.firstname
        emp_data['lastname'] = emp.lastname
        emp_data['email'] = emp.email
        emp_data['birth_date'] = emp.birth_date
        emp_data['department_id'] = emp.department_id
        emp_data['salary'] = emp.salary
        emp_data['role_id'] = emp.role_id
        dep_data['employees'].append(emp_data)
    return jsonify({'department': dep_data})


@app.route('/dep', methods=['POST'])
def create_department():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    if 'title' not in request.json:
        return make_response('Insufficient data in request', 400)
    if 'salary' not in request.json:
        return make_response('Insufficient data in request', 400)
    data = request.get_json()
    deps = Department.query.all()
    ids = [dep.id for dep in deps]
    dep_id = max(ids) + 1
    new_dep = Department(id=dep_id,
                         title=data['title'],
                         salary=data['salary'],
                         employees=[])
    db.session.add(new_dep)
    db.session.commit()
    return make_response('Department created', 201)


@app.route('/dep/<int:dep_id>', methods=['PATCH'])
def patch_department(dep_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    dep = Department.query.get(dep_id)

    if not dep:
        return make_response('Department not found', 404)

    data = request.get_json()
    if 'title' in data:
        dep.title = data['title']
    db.session.commit()
    return jsonify({'message': 'Department updated'})


@app.route('/dep/<int:dep_id>', methods=['DELETE'])
def delete_department(dep_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    dep = Department.query.get(dep_id)

    if not dep:
        return make_response('Department not found', 404)

    db.session.delete(dep)
    db.session.commit()
    return jsonify({'message': 'Department deleted'})


@app.route('/deps/search/<que>', methods=['GET'])
def search_deps(que):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    departments = Department.query.filter(Department.title.contains(que)).all()
    output = []
    for dep in departments:
        dep_data = dict()
        dep_data['id'] = dep.id
        dep_data['title'] = dep.title
        dep_data['employees'] = []
        for emp in dep.employees:
            emp_data = dict()
            emp_data['salary'] = emp.salary
            dep_data['employees'].append(emp_data)
        output.append(dep_data)
    return jsonify({'departments': output})


@app.route('/reqs', methods=['GET'])
def requests_list():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)
    reqs = eval(f'db.session.query(Request, Employee).filter({request.json["filter"]}).all()')
    output = []
    for req in reqs:
        req_data = dict()
        req_data['id'] = req[0].id
        req_data['status'] = req[0].status
        req_data['sender_id'] = req[1].id
        req_data['firstname'] = req[1].firstname
        req_data['lastname'] = req[1].lastname
        output.append(req_data)
    return jsonify({'reqs': output})


@app.route('/req/<int:req_id>', methods=['GET'])
def get_request(req_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)

    req = Request.query.get(req_id)
    if not req:
        return make_response('Request not found', 404)

    req_data = dict()
    req_data['id'] = req.id
    req_data['sender'] = req.sender
    req_data['change_department_id'] = req.change_department_id
    req_data['increase_salary'] = req.increase_salary
    req_data['status'] = req.status

    return jsonify({'req': req_data})


@app.route('/req', methods=['POST'])
def create_request():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)

    if ('sender' not in request.json
        or 'change_department_id' not in request.json
        or 'increase_salary' not in request.json):
        return make_response('Insufficient data in request', 400)
    data = request.get_json()

    new_req = Request(sender=data['sender'],
                      change_department_id=data['change_department_id'],
                      increase_salary=data['increase_salary'],
                      status=0)
    db.session.add(new_req)
    db.session.commit()
    return jsonify({'message': 'new request created'})


@app.route('/req/<int:req_id>', methods=['PATCH'])
def patch_request(req_id):
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'token' not in request.json:
        return make_response('No token in request', 400)
    valid = validate_token(request.json['token'])
    if valid.status_code != 200:
        return make_response(valid.response, valid.status_code)

    req = Request.query.get(req_id)

    if not req:
        return make_response('Request not found', 404)

    data = request.get_json()
    if 'status' in data:
        req.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Request updated'})


@app.route('/api_login', methods=['GET', 'POST'])
def login():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if 'email' not in request.json or 'password' not in request.json:
        return make_response('Insufficient data in request', 400)
    email = request.json['email']
    password = request.json['password']
    if not email or not password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    emp = Employee.query.filter_by(email=email).first()
    

    if not emp:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(emp.password, password):
        token = jwt.encode({'id': emp.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token,
                        'current_user_id': emp.id,
                        'department_id': emp.department_id,
                        'role_id': emp.role_id})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/api_register', methods=['GET', 'POST'])
def register():
    if not request.json:
        return make_response('Insufficient data in request', 400)
    if ('firstname' not in request.json
            or 'lastname' not in request.json
            or 'email' not in request.json
            or 'password' not in request.json
            or 'dep_title' not in request.json
            or 'birth_date' not in request.json):
        return make_response('Insufficient data in request', 400)
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']
    dep_title = request.json['dep_title']
    birth_date = request.json['birth_date']
    role_id = 2
    if (not firstname
            or not lastname
            or not email
            or not password
            or not dep_title
            or not birth_date):
        return make_response('Insufficient data in request', 400)
    hashed_password = generate_password_hash(password).decode('ascii')
    dep = Department.query.filter_by(title=dep_title).first()
    employee = Employee(firstname=firstname,
                        lastname=lastname,
                        birth_date=birth_date,
                        email=email,
                        password=hashed_password,
                        department_id=dep.id,
                        role_id=role_id,
                        salary=dep.salary)
    db.session.add(employee)
    db.session.commit()
    return make_response('Employee registered', 201)


if __name__ == '__main__':
    app.run(debug=True)
