from flask import render_template, request, abort, jsonify
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import desc, and_
from sqlalchemy.sql import null
from sqlalchemy.exc import IntegrityError, InvalidRequestError

import json
import datetime
from hashlib import sha1
from time import time
from werkzeug.datastructures import ImmutableMultiDict

from danarbu import app, db, models
from danarbu.forms import SearchForm


def is_relevant(field, enabled=True):
    if enabled and field.data != None and len(field.data) > 0:
        return True
    return False


def generate_hash():
    for i in range(11):
        try:
            new_hash = sha1(bytes("{}".format(time()), "utf-8")).hexdigest()[:10]
            tinyurl = models.Tinyurl(
                hashtime=new_hash,
                obj="",
                visited=0,
                visited_at=datetime.datetime.utcnow(),
            )
            db.session.add(tinyurl)
            db.session.commit()
            break
        except IntegrityError:
            continue
        except InvalidRequestError:
            continue
        except Exception as e:
            new_hash = "ekkiVistad"
            break

        if i == 10:
            new_hash = "ekkiVistad"
            break

    return new_hash


@app.route("/", methods=["GET", "POST"])
@app.route("/<request_hash>", methods=["GET", "POST"])
def root(request_hash=None):
    new_hash = generate_hash()
    execute_search = False

    if request.method == "POST":
        tinyurl = db.session.query(models.Tinyurl).get(request_hash)
        tinyurl.obj = json.dumps(request.form)
        db.session.commit()
        execute_search = True
    elif request.method == "GET" and request_hash is not None:
        tinyurl = db.session.query(models.Tinyurl).get(request_hash)
        try:
            request.form = ImmutableMultiDict(json.loads(tinyurl.obj))
            tinyurl.visited = tinyurl.visited + 1
            tinyurl.visited_at = datetime.datetime.utcnow()
            db.session.commit()
        except:
            abort(404)
        execute_search = True

    # Clean old non-visited entries from the tinyurl table.
    current_time = datetime.datetime.utcnow()
    tinyurl_delete = current_time - datetime.timedelta(weeks=30)
    db.session.query(models.Tinyurl).filter(
        models.Tinyurl.visited_at < tinyurl_delete
    ).filter(models.Tinyurl.visited <= 1).delete()
    db.session.commit()

    search_form = SearchForm(request.form)

    syslur = [("", "")]
    soknir = [("", "")]
    baeir = [("", "")]
    for (sysla,) in (
        db.session.query(models.Danarbu.sysla_heiti)
        .distinct()
        .order_by(models.Danarbu.sysla_heiti)
        .all()
    ):
        syslur.append((sysla, sysla))
    search_form.sysla_select.choices = syslur

    search_form.sokn_select.render_kw = {"disabled": True}
    if is_relevant(search_form.sysla_select):
        for (sokn,) in (
            db.session.query(models.Danarbu.sokn_heiti)
            .filter(models.Danarbu.sysla_heiti == search_form.sysla_select.data)
            .distinct()
            .order_by(models.Danarbu.sokn_heiti)
            .all()
        ):
            soknir.append((sokn, sokn))
        search_form.sokn_select.render_kw = {"disabled": False}

    search_form.baer_select.render_kw = {"disabled": True}
    if is_relevant(search_form.sokn_select):
        for (baer,) in (
            db.session.query(models.Danarbu.baer_heiti)
            .filter(
                and_(
                    models.Danarbu.sysla_heiti == search_form.sysla_select.data,
                    models.Danarbu.sokn_heiti == search_form.sokn_select.data,
                )
            )
            .distinct()
            .order_by(models.Danarbu.baer_heiti)
            .all()
        ):
            baeir.append((baer, baer))
        search_form.baer_select.render_kw = {"disabled": False}

    search_form.sokn_select.choices = soknir
    search_form.baer_select.choices = baeir

    if execute_search:
        page = request.args.get(get_page_parameter(), type=int, default=1)

        fulltext_columns = [
            models.Danarbu.nafn,
            models.Danarbu.stada,
            models.Danarbu.baer_heiti,
            models.Danarbu.sysla_heiti,
            models.Danarbu.sokn_heiti,
        ]
        if is_relevant(search_form.search_string):
            search_query = (
                db.session.query(
                    models.Danarbu,
                    models.MatchCol(
                        fulltext_columns, search_form.search_string.data
                    ).label("score"),
                )
                .filter(models.Match(fulltext_columns, search_form.search_string.data))
                .order_by(desc("score"), models.Danarbu.artal, models.Danarbu.nafn)
            )
        else:
            search_query = db.session.query(models.Danarbu).order_by(
                models.Danarbu.artal, models.Danarbu.nafn
            )

        if is_relevant(
            search_form.sysla_select, search_form.show_advanced_search.data == "true"
        ):
            search_query = search_query.filter(
                models.Danarbu.sysla_heiti == search_form.sysla_select.data
            )

        if is_relevant(
            search_form.sokn_select, search_form.show_advanced_search.data == "true"
        ):
            search_query = search_query.filter(
                models.Danarbu.sokn_heiti == search_form.sokn_select.data
            )

        if is_relevant(
            search_form.baer_select, search_form.show_advanced_search.data == "true"
        ):
            search_query = search_query.filter(
                models.Danarbu.baer_heiti == search_form.baer_select.data
            )

        if is_relevant(
            search_form.tegund_select, search_form.show_advanced_search.data == "true"
        ):
            if search_form.tegund_select.data == "danarbu":
                search_query = search_query.filter(
                    models.Danarbu.danarbu == models.Tilvist.til
                )
            elif search_form.tegund_select.data == "skiptabok":
                search_query = search_query.filter(
                    models.Danarbu.skiptabok == models.Tilvist.til
                )
            elif search_form.tegund_select.data == "lods":
                search_query = search_query.filter(
                    models.Danarbu.danarbu == models.Tilvist.lods
                )
            elif search_form.tegund_select.data == "uppbod":
                search_query = search_query.filter(
                    models.Danarbu.uppskrift == models.Tilvist.til
                )

        if is_relevant(
            search_form.ar_fra_input, search_form.show_advanced_search.data == "true"
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.artal >= int(search_form.ar_fra_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.ar_til_input, search_form.show_advanced_search.data == "true"
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.artal <= int(search_form.ar_til_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.mat_fra_input, search_form.show_advanced_search.data == "true"
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.mat >= int(search_form.mat_fra_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.mat_til_input, search_form.show_advanced_search.data == "true"
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.mat <= int(search_form.mat_til_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.nafn_input, search_form.show_advanced_search.data == "true"
        ):
            search_query = search_query.filter(
                models.Danarbu.nafn.like("%{}%".format(search_form.nafn_input.data))
            )

        if is_relevant(
            search_form.stada_input, search_form.show_advanced_search.data == "true"
        ):
            search_query = search_query.filter(
                models.Danarbu.stada.like(search_form.stada_input.data)
            )

        if is_relevant(
            search_form.kyn_select, search_form.show_advanced_search.data == "true"
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.kyn == int(search_form.kyn_select.data)
                )
            except:
                pass

        if is_relevant(
            search_form.aldur_fra_input, search_form.show_advanced_search.data == "true"
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.aldur >= int(search_form.aldur_fra_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.aldur_til_input, search_form.show_advanced_search.data == "true"
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.aldur <= int(search_form.aldur_til_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.faeding_fra_input,
            search_form.show_advanced_search.data == "true",
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.faeding_leit
                    >= int(search_form.faeding_fra_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.faeding_til_input,
            search_form.show_advanced_search.data == "true",
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.faeding_leit
                    <= int(search_form.faeding_til_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.andlat_fra_input,
            search_form.show_advanced_search.data == "true",
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.andlat_leit >= int(search_form.andlat_fra_input.data)
                )
            except:
                pass

        if is_relevant(
            search_form.andlat_til_input,
            search_form.show_advanced_search.data == "true",
        ):
            try:
                search_query = search_query.filter(
                    models.Danarbu.andlat_leit <= int(search_form.andlat_til_input.data)
                )
            except:
                pass

        print(
            str(search_query).replace(
                "%s", '"{}"'.format(search_form.search_string.data)
            )
        )
        search_query = search_query.paginate(
            page, app.config["DEFAULT_ITEMS_PER_PAGE"], False
        )
        pagination = Pagination(
            page=page,
            total=search_query.total,
            per_page=app.config["DEFAULT_ITEMS_PER_PAGE"],
            css_framework="bootstrap4",
            alignment="center",
        )
        if len(search_form.search_string.data) > 0:
            results = [result for result, score in search_query.items]
        else:
            results = search_query.items

        return render_template(
            "nidurstodur.html",
            search_form=search_form,
            show_advanced_search="show"
            if search_form.show_advanced_search.data == "true"
            else "",
            search_results=results,
            pagination=pagination,
            post_hash=new_hash,
            leit_active="active",
        )
    else:
        return render_template(
            "index.html",
            search_form=search_form,
            syslur=syslur,
            post_hash=new_hash,
            leit_active="active",
        )


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
        return "{}. {} {}".format(dagur, manudur_nofn[int(manudur)], ar)
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
    heimildir = []
    for db_heimild in db.session.query(models.Heimildir).filter(
        models.Heimildir.danarbu == danarbu.id
    ):
        heimild = dict(db_heimild.__dict__)
        if db_heimild.endanleg and len(db_heimild.endanleg) > 0:
            heimild["tengill"] = (
                "http://skjalaskrar.skjalasafn.is/b/" + db_heimild.endanleg
            )
        else:
            heimild["tengill"] = None

        heimild["myndir"] = []
        for mynd in (
            db.session.query(models.Myndir)
            .filter(models.Myndir.heimild == db_heimild.id)
            .order_by(models.Myndir.id)
        ):
            heimild["myndir"].append(mynd)
        heimildir.append(heimild)

    return render_template(
        "faersla.html", danarbu=danarbu, dags=dags, heimildir=heimildir
    )


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


@app.route("/stada")
def stada():
    prefix = request.args.get("q", type=str, default="")
    stodur = [
        stada
        for stada, in db.session.query(models.Danarbu.stada)
        .filter(models.Danarbu.stada != "")
        .filter(models.Danarbu.stada.like("%{}%".format(prefix)))
        .distinct()
        .order_by(models.Danarbu.stada)
        .all()
    ]
    return jsonify(stodur)


@app.route("/um")
def um():
    results = (
        db.session.query(models.UmVefinn).order_by(models.UmVefinn.id.desc()).first()
    )
    return render_template(
        "static.html", static_html=results.texti, um_vefinn_active="active"
    )


@app.route("/itarefni")
def itarefni():
    results = (
        db.session.query(models.Itarefni).order_by(models.Itarefni.id.desc()).first()
    )

    return render_template(
        "static.html", static_html=results.texti, itarefni_active="active"
    )


@app.route("/hjalp")
def hjalp():
    results = db.session.query(models.Hjalp).order_by(models.Hjalp.id.desc()).first()

    return render_template(
        "static.html", static_html=results.texti, hjalp_active="active"
    )
