from flask import render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
from danarbu import app, db, models
from danarbu.forms import SimpleSearchForm
from sqlalchemy import desc


@app.route("/", methods=["GET"])
def root():
    simple_form = SimpleSearchForm(request.args)
    if simple_form.validate():
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

        for result in results:
            result.heimildir = []
            for heimild in db.session.query(models.Heimildir).filter(
                models.Heimildir.danarbu == result.id
            ):
                result.heimildir.append(heimild)
        return render_template(
            "nidurstodur.html",
            search_form=simple_form,
            show_advanced_search="",
            search_results=results,
            pagination=pagination,
        )
    else:
        return render_template("index.html", search_form=simple_form)


@app.route("/itarleit")
def itarleit():
    return "Það er engin ítarleit ennþá."


@app.route("/myndir")
def myndir():
    danarbu_id = request.args.get("id", type=int, default=1)
    myndir = []
    for heimild in (
        models.Heimildir.query.filter(models.Heimildir.danarbu == danarbu_id)
        .order_by(models.Heimildir.id)
        .all()
    ):
        for mynd in (
            models.Myndir.query.filter(models.Myndir.heimild == heimild.id)
            .order_by(models.Myndir.id)
            .all()
        ):
            myndir.append(
                {
                    "tegund": heimild.tegund,
                    "endanleg": heimild.endanleg,
                    "slod": mynd.slod,
                }
            )
    if len(myndir) == 0:
        return "Engar myndir tilheyra þessari færslu."
    else:
        return render_template("myndir.html", myndir=myndir)
