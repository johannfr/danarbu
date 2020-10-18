from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SimpleSearchForm(FlaskForm):
    search_string = StringField("Leit")
    submit = SubmitField("Leita")
