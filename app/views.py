from flask import render_template, request
from app import app
from app import queries


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/leit", methods=["GET"])
def leit():
    search_string = request.args.get("leitarstrengur")
    return render_template(
        "nidurstodur.html",
        show_advanced_search="",
        search_string=search_string,
        search_results=queries.simple_search(search_string),
    )


@app.route("/itarleit")
def itarleit():
    return "Það er engin ítarleit ennþá."
