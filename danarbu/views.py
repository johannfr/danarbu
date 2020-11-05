from flask import render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import desc

from danarbu import app, db, models
from danarbu.forms import SimpleSearchForm


@app.route("/", methods=["GET"])
def root():
    simple_form = SimpleSearchForm(request.args)
    if simple_form.validate() and simple_form.search_string.data:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        fulltext_columns = [
            models.Danarbu.nafn,
            models.Danarbu.stada,
            models.Danarbu.baer_heiti,
            models.Danarbu.sysla_heiti,
            models.Danarbu.sokn_heiti,
        ]
        search_query = (
            db.session.query(
                models.Danarbu,
                models.MatchCol(fulltext_columns, simple_form.search_string.data).label(
                    "score"
                ),
            )
            .filter(models.Match(fulltext_columns, simple_form.search_string.data))
            .order_by(desc("score"))
            .paginate(page, app.config["DEFAULT_ITEMS_PER_PAGE"], False)
        )
        pagination = Pagination(
            page=page,
            total=search_query.total,
            per_page=app.config["DEFAULT_ITEMS_PER_PAGE"],
            css_framework="bootstrap4",
            alignment="center",
        )
        results = [result for result, score in search_query.items]

        return render_template(
            "nidurstodur.html",
            search_form=simple_form,
            show_advanced_search="",
            search_results=results,
            pagination=pagination,
        )
    else:
        return render_template("index.html", search_form=simple_form)


def parse_date(date):
    try:
        dagur, manudur, ar = date.split(".")
        manudur_nofn = {
            1: "janúar",
            2: "febúar",
            3: "mars",
            4: "apríl",
            5: "maí",
            6: "júní",
            7: "júlí",
            8: "ágúst",
            9: "september",
            10: "október",
            11: "nóvember",
            12: "desember",
        }
        return "{}. {}, {}".format(dagur, manudur_nofn[int(manudur)], ar)
    except ValueError:
        pass
    try:
        return int(date)  # Stundum bara artal
    except ValueError or TypeError:
        pass
    return None


@app.route("/faersla", methods=["GET"])
def faersla():
    danarbu_id = request.args.get("id", type=int, default=1)
    danarbu = db.session.query(models.Danarbu).get(danarbu_id)
    dags = {}
    dags["andlat"] = parse_date(danarbu.andlat)
    dags["faeding"] = parse_date(danarbu.faeding)
    dags["skraning"] = parse_date(danarbu.skraning)
    dags["uppbod"] = parse_date(danarbu.uppbod)
    dags["skipti"] = parse_date(danarbu.skipti)
    danarbu.heimildir = []
    for heimild in db.session.query(models.Heimildir).filter(
        models.Heimildir.danarbu == danarbu.id
    ):
        if heimild.endanleg and len(heimild.endanleg) > 0:
            heimild_tengill = "http://skjalaskrar.skjalasafn.is/b/" + heimild.endanleg
        else:
            heimild_tengill = "http://skjalaskrar.skjalasafn.is/b/" + heimild.upprunaleg
        heimild.myndir = []
        for mynd in (
            db.session.query(models.Myndir)
            .filter(models.Myndir.heimild == heimild.id)
            .order_by(models.Myndir.id)
        ):
            heimild.myndir.append(mynd)
        danarbu.heimildir.append(heimild)

    return render_template(
        "faersla.html", danarbu=danarbu, dags=dags, heimild_tengill=heimild_tengill
    )


@app.route("/itarleit")
def itarleit():
    return "Það er engin ítarleit ennþá."


@app.route("/myndir")
def myndir():
    heimild_id = request.args.get("id", type=int, default=1)
    open_index = request.args.get("index", type=int, default=0)

    heimild = db.session.query(models.Heimildir).get(heimild_id)
    myndir = []
    for mynd in (
        models.Myndir.query.filter(models.Myndir.heimild == heimild_id)
        .order_by(models.Myndir.id)
        .all()
    ):
        myndir.append(
            {
                "slod": mynd.slod,
            }
        )
    if len(myndir) == 0:
        return "Engar myndir tilheyra þessari færslu."
    else:
        return render_template(
            "myndir.html", myndir=myndir, upphaf=open_index, heimild=heimild
        )
