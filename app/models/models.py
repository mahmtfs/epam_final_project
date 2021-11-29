from app.extensions import db
import requests


class Employee(db.Model):
    __tablename__ = 'employee'
    __searchable__ = ['firstname', 'lastname']

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    birth_date = db.Column(db.DATE, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    salary = db.Column(db.Float)


class Department(db.Model):
    __tablename__ = 'department'
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    #salary = db.Column(db.Float, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)

    def get_departments(self):
        response = requests.get(self.api_host_name + r'/department/' + str(3))
        if response.ok:
            return response.text
        else:
            return 'Bad response!'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='role', lazy=True)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    #recipient = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    change_department_id = db.Column(db.Integer)
    increase_salary = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
