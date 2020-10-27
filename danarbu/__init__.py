from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from danarbu.config import Config
from sqlalchemy import text, bindparam

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
from danarbu import views, models

Bootstrap(app)
