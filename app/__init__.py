#!/usr/bin/python3
"""
this is the initialization of my application
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager
from flask_mail import Mail


# app initialization
app = Flask(__name__)

# initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#the configuration for the app
app.config.from_object(Config)

# database initialization
db = SQLAlchemy()
db.__init__(app)
migrate = Migrate(app, db)


#initialize mail
mail = Mail(app)

from app.routes import route
