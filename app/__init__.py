from flask import Flask
from app.views import general, auth, current_user, redirect, url_for
from app.models import Department


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rinat:jojo1337@localhost/departments_project'
app.config['SECRET_KEY'] = 'supersecret'
app.config['WHOOSH_BASE'] = 'whoosh'
app.register_blueprint(general)
app.register_blueprint(auth)


from .extensions import db, bcr, login_manager


db.init_app(app)
bcr.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import Employee, Department, Role


class MyModelView(ModelView):
    def is_accessible(self):
        try:
            if current_user.role.id == 4:
                return True
        except AttributeError:
            return None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            if current_user.role.id == 4:
                return True
        except AttributeError:
            return None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


admin = Admin(app, index_view=MyAdminIndexView())

admin.add_view(MyModelView(Employee, db.session))
admin.add_view(MyModelView(Department, db.session))
admin.add_view(MyModelView(Role, db.session))
