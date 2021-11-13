from flask_login import UserMixin
from app.extensions import db


class Employee(db.Model, UserMixin):
    __tablename__ = 'employee'
    __searchable__ = ['firstname', 'lastname']

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)


class Department(db.Model):
    __tablename__ = 'department'
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    salary = db.Column(db.Numeric, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='role', lazy=True)
