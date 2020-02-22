from flask import Flask
from config import Configuration

from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
app = Flask(__name__)
sslify = SSLify(app)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
### db = app.config['SQLALCHEMY_DATABASE_URI']
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
### Flask-security

from models import *
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



