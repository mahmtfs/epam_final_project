from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
bcr = Bcrypt()
migrate = Migrate()
mail = Mail()
