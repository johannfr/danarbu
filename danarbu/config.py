from os import getenv


class Config(object):
    SECRET_KEY = getenv("DANARBU_CSRF_SECRET") or "dev-secret"
    SQLALCHEMY_DATABASE_URI = getenv("DANARBU_DBURI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_ITEMS_PER_PAGE = 25
    GA_ID = getenv("DANARBU_GA_ID") or "dev-ga-id"
