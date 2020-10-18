from os import getenv


class Config(object):
    SECRET_KEY = getenv("DANARBU_CSRF_SECRET") or "dev-secret"
    SQLALCHEMY_DATABASE_URI = getenv("DANARBU_DBURI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
