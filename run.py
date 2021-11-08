from flask_admin.contrib.sqla import ModelView
from app import app
from app import admin
from app.db.db import db
from app.rest.models import Employee, Department, Role


admin.add_view(ModelView(Employee, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ModelView(Role, db.session))


if __name__ == '__main__':
    app.run(debug=True)
