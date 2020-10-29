from flask import current_app, redirect, render_template, session, url_for

from .. import db
from ..models import User
from . import main
from .forms import NameForm


@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
        else:
            session["known"] = True
        session["name"] = form.name.data
        return redirect(url_for(".index"))
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )


@main.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")


@main.route("/fridge", methods=["GET", "POST"])
def fridge():
    return render_template("fridge.html")


@main.route("/list", methods=["GET", "POST"])
def list():
    return render_template("list.html")
