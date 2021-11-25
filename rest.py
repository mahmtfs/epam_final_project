import jwt
import datetime
from flask import request, jsonify, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from functools import wraps
from app import app
from app import db
from app.models.models import (Employee,
                               Department,
                               Request)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Employee.query.get(data['id'])
        except:
            return jsonify({'message': 'token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/emps', methods=['GET'])
@token_required
def get_all_employees(current_user):

    if current_user.role_id != 4:
        return jsonify({'message': 'Permission denied'})

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
@token_required
def get_employee(current_user, emp_id):
    if current_user.role_id != 4:
        return jsonify({'message': 'Permission denied'})

    emp = Employee.query.get(emp_id)

    if not emp:
        return jsonify({'message': 'Employee not found'})

    emp_data = dict()
    emp_data['id'] = emp.id
    emp_data['firstname'] = emp.firstname
    emp_data['lastname'] = emp.lastname
    emp_data['email'] = emp.email
    emp_data['birth_date'] = emp.birth_date
    emp_data['department_id'] = emp.department_id
    emp_data['salary'] = emp.salary
    emp_data['role_id'] = emp.role_id

    return jsonify({'user': emp_data})


@app.route('/emp', methods=['POST'])
@token_required
def create_employee(current_user):
    if current_user.role_id != 4:
        return jsonify({'message': 'Permission denied'})
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'])

    new_emp = Employee(firstname=data['firstname'],
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
@token_required
def patch_employee(current_user, emp_id):
    if current_user.role_id != 4:
        return jsonify({'message': 'Permission denied'})
    emp = Employee.query.get(emp_id)

    if not emp:
        return jsonify({'message': 'Employee not found'})

    data = request.get_json()
    if data['password']:
        emp.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({'message': 'Employee updated'})


@app.route('/emp/<int:emp_id>', methods=['DELETE'])
@token_required
def delete_employee(current_user, emp_id):
    if current_user.role_id != 4:
        return jsonify({'message': 'Permission denied'})
    emp = Employee.query.get(emp_id)

    if not emp:
        return jsonify({'message': 'Employee not found'})

    db.session.delete(emp)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'})


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    emp = Employee.query.filter_by(email=auth.username).first()

    if not emp:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(emp.password, auth.password):
        token = jwt.encode({'id': emp.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


if __name__ == '__main__':
    app.run(debug=True)
