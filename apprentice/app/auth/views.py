from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, SignupForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    """On form submission(POST), logs the user in if it exists and the password is valid.

    Returns:
        On a GET request:
            Returns the rendered template for the login page.
        On a POST request (form submission):
            If the login form was presented to prevent un‐authorized access to a URL, redirects to the original URL.
            Otherwise, redirects to the the homepage.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("User does not exist!")
        elif not user.verify_password(form.password.data):
            flash("Invalid password!")
        else:
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """Logs out the currently logged in user.

    Returns:
        Redirects to the homepage.
    """
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """On form submission(POST), adds the new user to the database (if fields are valid)

    Returns:
        On a GET request, returns the rendered template for the signup page.
        On a POST request (form submission), redirects to the login page.
    """
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
        return redirect(url_for("auth.login"))
    return render_template("signup.html", form=form)
