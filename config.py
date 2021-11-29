import os
import secrets


DEBUG = True
TESTING = False
SECRET_KEY = secrets.token_hex(16)

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

URL = 'https://pure-caverns-26611.herokuapp.com'
