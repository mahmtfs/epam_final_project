import os
import secrets


DEBUG = False
TESTING = False
SECRET_KEY = os.getenv('SECRET_KEY')
if (os.getenv("DATABASE_URL")[0] == 'm'):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
else:
    SQLALCHEMY_DATABASE_URI = f'postgresql{os.getenv("DATABASE_URL")[8:]}'


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = DEBUG
MAIL_USERNAME = os.getenv('MAIL_USER')
MAIL_PASSWORD = os.getenv('MAIL_PASS')
MAIL_DEFAULT_SENDER = MAIL_USERNAME
MAIL_MAX_EMAILS = None
MAIL_SUPPRESS_SEND = TESTING
MAIL_ASCII_ATTACHMENTS = False

RESET_PASSWORD_MESSAGE = 'To reset your password, visit the following link:\n'
RESET_PASSWORD_WARNING = '\nIf you did not make this request, simply ignore this email.'

URL = 'https://departments-flask-app.herokuapp.com'

SQLALCHEMY_POOL_RECYCLE = 90

ADMIN_ROLE_ID = 1
REGULAR_ROLE_ID = 2
