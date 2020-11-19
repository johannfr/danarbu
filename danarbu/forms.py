from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import required, optional


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    show_advanced_search = HiddenField(default="true")
    search_string = StringField("Leit", [optional()])
    sysla_select = SelectField("Sýsla", [optional()])
    sokn_select = SelectField("Sókn", [optional()])
    baer_select = SelectField("Bær", [optional()])
    ar_fra_input = StringField("Ár (frá)", [optional()])
    ar_til_input = StringField("Ár (til)", [optional()])
    nafn_input = StringField("Nafn", [optional()])
    stada_input = StringField("Staða", [optional()])
    kyn_select = SelectField(
        "Kyn",
        [optional()],
        choices=[("", ""), ("1", "KK"), ("2", "KVK"), ("3", "Hjón")],
    )
    aldur_fra_input = StringField("Aldur (frá)", [optional()])
    aldur_til_input = StringField("Aldur (til)", [optional()])
    tegund_select = SelectField(
        "Tegund",
        [optional()],
        choices=[
            ("", ""),
            ("danarbu", "Dánarbú"),
            ("skiptabok", "Skiptabók"),
            ("lods", "Lóðseðlar"),
            ("uppbod", "Uppboð"),
        ],
    )
    faeding_fra_input = StringField("Fæðing (frá)", [optional()])
    faeding_til_input = StringField("Fæðing (til)", [optional()])
    andlat_fra_input = StringField("Andlát (frá)", [optional()])
    andlat_til_input = StringField("Andlát (til)", [optional()])
    mat_fra_input = StringField("Mat (frá)", [optional()])
    mat_til_input = StringField("Mat (til)", [optional()])
