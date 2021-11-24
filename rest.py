from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from app import app
from app.models.models import Employee, Department, Request
from app.extensions import db
from config import DEBUG


api = Api(app)
user_put_args = reqparse.RequestParser()
user_update_args = reqparse.RequestParser()
department_put_args = reqparse.RequestParser()
department_update_args = reqparse.RequestParser()
request_put_args = reqparse.RequestParser()
request_update_args = reqparse.RequestParser()

user_put_args.add_argument('firstname', type=str, required=True)
user_put_args.add_argument('lastname', type=str, required=True)
user_put_args.add_argument('email', type=str, required=True)
user_put_args.add_argument('department_id', type=int, required=True)

user_update_args.add_argument('firstname', type=str)
user_update_args.add_argument('lastname', type=str)
user_update_args.add_argument('email', type=str)
user_update_args.add_argument('department_id', type=int)

department_put_args.add_argument('title', type=str, required=True)

department_update_args.add_argument('title', type=str)

request_put_args.add_argument('sender', type=int, required=True)
request_put_args.add_argument('change_department_id', type=int, required=True)
request_put_args.add_argument('increase_salary', type=int, required=True)
request_put_args.add_argument('status', type=int, required=True)

request_update_args.add_argument('sender', type=int)
request_update_args.add_argument('change_department_id', type=int)
request_update_args.add_argument('increase_salary', type=int)
request_update_args.add_argument('status', type=int)

user_fields = {
    'id': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'department_id': fields.Integer,
    'role_id': fields.Integer,
    'salary': fields.Float
}

department_fields = {
    'id': fields.Integer,
    'title': fields.String
}

request_fields = {
    'id': fields.Integer,
    'sender': fields.Integer,
    'change_department_id': fields.Integer,
    'increase_salary': fields.Integer,
    'status': fields.Integer
}


class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        result = Employee.query.get(user_id)
        if not result:
            abort(404, message='There is no employee with such id')
        return result

    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        result = Employee.query.get(user_id)
        if result:
            abort(409, message='There is already an employee with such id')
        department = Department.query.get(args['department_id'])
        if not department:
            abort(404, message='There is no department with such id')
        employee = Employee(id=user_id,
                            firstname=args['firstname'],
                            lastname=args['lastname'],
                            birth_date='1990-11-11',
                            email=args['email'],
                            password='...',
                            department_id=args['department_id'],
                            role_id=3,
                            salary=0)
        db.session.add(employee)
        db.session.commit()
        return employee, 201

    @marshal_with(user_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = Employee.query.get(user_id)
        if not result:
            abort(404, message='There is no employee with such id')
        if args['department_id']:
            department = Department.query.get(args['department_id'])
            if not department:
                abort(404, message='There is no department with such id')
            else:
                result.department_id = args['department_id']
        if args['firstname']:
            result.firstname = args['firstname']
        if args['lastname']:
            result.lastname = args['lastname']
        if args['email']:
            result.email = args['email']
        db.session.commit()
        return result

    @marshal_with(user_fields)
    def delete(self, user_id):
        result = Employee.query.get(user_id)
        if not result:
            abort(404, message='There is no user with such id')
        db.session.delete(result)
        db.session.commit()
        return result


class Dep(Resource):
    @marshal_with(department_fields)
    def get(self, department_id):
        result = Department.query.get(department_id)
        if not result:
            abort(404, message='There is no department with such id')
        return result

    @marshal_with(department_fields)
    def put(self, department_id):
        args = department_put_args.parse_args()
        result = Department.query.get(department_id)
        if result:
            abort(409, message='There is already a department with such id')
        department = Department(id=department_id,
                                title=args['title'])
        db.session.add(department)
        db.session.commit()
        return department, 201

    @marshal_with(department_fields)
    def patch(self, department_id):
        args = department_update_args.parse_args()
        result = Department.query.get(department_id)
        if not result:
            abort(404, message='There is no department with such id')
        if args['title']:
            result.title = args['title']
        db.session.commit()
        return result

    @marshal_with(department_fields)
    def delete(self, department_id):
        result = Department.query.get(department_id)
        if not result:
            abort(404, message='There is no department with such id')
        db.session.delete(result)
        db.session.commit()
        return result


class Req(Resource):
    @marshal_with(request_fields)
    def get(self, request_id):
        result = Request.query.get(request_id)
        if not result:
            abort(404, message='There is no request with such id')
        return result

    @marshal_with(request_fields)
    def put(self, request_id):
        args = request_put_args.parse_args()
        result = Request.query.get(request_id)
        if result:
            abort(409, message='There is already a request with such id')
        sender = Employee.query.get(args['sender'])
        if not sender:
            abort(404, message='There is no employee with such id')
        department = Department.query.get(args['change_department_id'])
        if not department:
            abort(404, message='There is no department with such id')
        if not (args['status'] in [0, 1, 2]):
            abort(404, message='There is no such status of request')
        request = Request(id=request_id,
                          sender=args['sender'],
                          change_department_id=args['change_department_id'],
                          increase_salary=args['increase_salary'],
                          status=args['status'])
        db.session.add(request)
        db.session.commit()
        return request, 201

    @marshal_with(request_fields)
    def patch(self, request_id):
        args = request_update_args.parse_args()
        result = Request.query.get(request_id)
        if not result:
            abort(404, message='There is no request with such id')
        if args['sender']:
            sender = Employee.query.get(args['sender'])
            if not sender:
                abort(404, message='There is no employee with such id')
            result.sender = args['sender']
        if args['change_department_id']:
            department = Department.query.get(args['change_department_id'])
            if not department:
                abort(404, message='There is no department with such id')
            result.change_department_id = args['change_department_id']
        if args['increase_salary']:
            result.increase_salary = args['increase_salary']
        if args['status']:
            if not (args['status'] in [0, 1, 2]):
                abort(404, message='There is no such status of request')
            result.status = args['status']
        db.session.commit()
        return result

    @marshal_with(request_fields)
    def delete(self, request_id):
        result = Request.query.get(request_id)
        if not result:
            abort(404, message='There is no request with such id')
        db.session.delete(result)
        db.session.commit()
        return result


api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Dep, '/dep/<int:department_id>')
api.add_resource(Req, '/req/<int:request_id>')

if __name__ == '__main__':
    app.run(debug=DEBUG, port=80)
