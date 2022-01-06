from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from flask_caching import Cache


from random import randint
import base64
import os
import pytz
import requests
import math


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='Ecom', template_mode='bootstrap3')


app.config['CACHE_TYPE'] = "SimpleCache"
cache = Cache(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/ecom'
app.secret_key = 'some key'

app.config['UPLOAD_FOLDER'] = 'static/imagesfolder'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

from routes import routes
