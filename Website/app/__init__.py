from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# Handles all migrations.
migrate = Migrate(app, db)
#logging.basicConfig(level=logging.DEBUG, filename="events.log") # basic template for logging

from app import views, models
from .models import User

# from flask_login import LoginManager
# login = LoginManager()
# login.init_app(app)

# @login.user_loader
# def loadUser(id):
#     return User.query.get(int(id))