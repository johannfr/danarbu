from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, IntegerField
from wtforms.validators import required, optional


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_string = StringField("Leit", [optional()])
    sysla_select = SelectField("Sýsla", [optional()])
    sokn_select = SelectField("Sókn", [optional()])
    baer_select = SelectField("Bær", [optional()])
    ar_fra_input = IntegerField(
        "Ár (frá)",
        [optional()],
        render_kw={"type": "number", "min": "1500", "max": "2000"},
    )
    ar_til_input = IntegerField(
        "Ár (til)",
        [optional()],
        render_kw={"type": "number", "min": "1500", "max": "2000"},
    )
    nafn_input = StringField("Nafn", [optional()])
    stada_input = StringField("Staða", [optional()])
    kyn_select = SelectField(
        "Kyn",
        [optional()],
        choices=[("", ""), ("1", "KK"), ("2", "KVK"), ("3", "Hjón")],
    )
    aldur_fra_input = StringField(
        "Aldur (frá)",
        [optional()],
        render_kw={"type": "number", "min": "0", "max": "200"},
    )
    aldur_til_input = StringField(
        "Aldur (til)",
        [optional()],
        render_kw={"type": "number", "min": "0", "max": "200"},
    )
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
    faeding_fra_input = StringField(
        "Fæðing (frá)",
        [optional()],
        render_kw={"type": "number", "min": "1500", "max": "2000"},
    )
    faeding_til_input = StringField(
        "Fæðing (til)",
        [optional()],
        render_kw={"type": "number", "min": "1500", "max": "2000"},
    )
    mat_fra_input = IntegerField(
        "Mat (frá)",
        [optional()],
        render_kw={"type": "number", "min": "0"},
    )
    mat_til_input = IntegerField(
        "Mat (til)",
        [optional()],
        render_kw={"type": "number", "min": "0"},
    )
    items_per_page_select = SelectField(
        "Fjöldi á síðu",
        choices=[
            ("25", "25"),
            ("50", "50"),
            ("75", "75"),
            ("100", "100"),
            ("99999999999", "Allar"),
        ],
    )
