from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import required, optional


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    show_advanced_search = HiddenField(default="false")
    search_string = StringField("Leit", [optional()])
    sysla_select = SelectField("Sýsla", [optional()])
    sokn_select = SelectField("Sókn", [optional()])
    baer_select = SelectField("Bær", [optional()])
