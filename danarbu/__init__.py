from flask import Flask
from flask_bs4 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from danarbu.config import Config
from sqlalchemy import text, bindparam
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
from danarbu import views, models

Bootstrap(app)
DebugToolbarExtension(app)
