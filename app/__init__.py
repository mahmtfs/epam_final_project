import datetime
from flask import Flask, redirect, url_for, session
import config
from app.views.views import general, auth
from .extensions import db, bcr, migrate, mail


def create_app():
    app = Flask(__name__)
    app.permanent_session_lifetime = datetime.timedelta(days=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amdyotrrmexbtb:ac783f5b7d1ae8509c6c8a271ec6fe02b7f44adf35daabc10929c0508e5ac547@ec2-52-211-233-176.eu-west-1.compute.amazonaws.com:5432/d3v8v9i8okp9sc'
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['WHOOSH_BASE'] = 'whoosh'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_RECYCLE'] = config.SQLALCHEMY_POOL_RECYCLE

    app.config['MAIL_SERVER'] = config.MAIL_SERVER
    app.config['MAIL_PORT'] = config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
    app.config['MAIL_DEBUG'] = config.MAIL_DEBUG
    app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
    app.config['MAIL_MAX_EMAILS'] = config.MAIL_MAX_EMAILS
    app.config['MAIL_SUPPRESS_SEND'] = config.MAIL_SUPPRESS_SEND
    app.config['MAIL_ASCII_ATTACHMENTS'] = config.MAIL_ASCII_ATTACHMENTS

    app.register_blueprint(general)
    app.register_blueprint(auth)
    return app


app = create_app()
db.init_app(app)
bcr.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)

from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models.models import Employee, Department, Role


class MyModelView(ModelView):
    def __init__(self, model, session, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        super(MyModelView, self).__init__(model, session)


    def is_accessible(self):
        try:
            if session['role_id'] == 4:
                return True
        except AttributeError:
            return None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            if session['role_id'] == 4:
                return True
        except KeyError:
            return None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class BackHomeView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('general.departments_page'))


admin = Admin(app, index_view=MyAdminIndexView())

admin.add_view(MyModelView(Employee, db.session, column_list=['id',
                                                              'firstname',
                                                              'lastname',
                                                              'email',
                                                              'birth_date',
                                                              'password',
                                                              'department_id',
                                                              'role_id']))
admin.add_view(MyModelView(Department, db.session, column_list=['id',
                                                                'title',
                                                                'salary',
                                                                'employees']))
admin.add_view(MyModelView(Role, db.session, column_list=['id',
                                                          'name',
                                                          'employees']))
admin.add_view(BackHomeView(name='Go Back Home', endpoint='/back'))
