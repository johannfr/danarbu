from flask import render_template, request, redirect
from danarbu import app
from danarbu.forms import SimpleSearchForm


@app.route("/", methods=["GET", "POST"])
def root():
    simple_form = SimpleSearchForm()
    if simple_form.validate_on_submit():
        return render_template(
            "nidurstodur.html",
            search_form=simple_form,
            show_advanced_search="",
            search_results=[],  # queries.simple_search(simple_form.search_string.data),
        )
    else:
        return render_template("index.html", search_form=simple_form)


@app.route("/itarleit")
def itarleit():
    return "Það er engin ítarleit ennþá."
