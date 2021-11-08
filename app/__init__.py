from flask import Flask
from flask_admin import Admin
from .views.general import general
from .auth.auth import auth


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rinat:jojo1337@localhost/departments_project'
    app.config['SECRET_KEY'] = 'supersecret'
    app.register_blueprint(general)
    app.register_blueprint(auth)
    return app


app = create_app()

admin = Admin(app)
