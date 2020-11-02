from flask import current_app, redirect, render_template, session, url_for

from .. import db
from ..models import User
from . import main
from .forms import NameForm
import json
import os


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
    # assume given data is like example.json
    cwd = os.getcwd()
    datapath = os.path.join(cwd, 'app/example.json')
    with open(datapath) as f:
        dict_dump = json.load(f)    
    results = True
    num_results = 1
    recipe_name = dict_dump['name']
    recipe_pic = dict_dump['image']
    recipe_url = dict_dump['url']
    recipe_desc = dict_dump['description']

    return render_template("search.html", 
        search_results=results,
        num_res=num_results,
        name=recipe_name,
        image=recipe_pic,
        url=recipe_url,
        description=recipe_desc    
    )


@main.route("/fridge", methods=["GET", "POST"])
def fridge():
    return render_template("fridge.html")


@main.route("/list", methods=["GET", "POST"])
def list():
    return render_template("list.html")
