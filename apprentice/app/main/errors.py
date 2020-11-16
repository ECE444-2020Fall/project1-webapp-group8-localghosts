from flask import render_template

from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    """Handler for 404 error.

    Returns:
        The rendered template for 404.html.
    """
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Handler for 500 error.

     Returns:
         The rendered template for 500.html.
    """
    return render_template("500.html"), 500
