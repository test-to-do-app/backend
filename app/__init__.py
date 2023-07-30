from flask import Flask
from flask_cors import CORS
from peewee import SqliteDatabase

import config

# Приложение
app = Flask(__name__)
app.config.from_object(config.Config)
cors = CORS(app, resources={"*": {"origins": "*"}})

# БД
db = SqliteDatabase(app.config['SQLITE_DB_NAME'])
# db = Database(app)

from .views import *
