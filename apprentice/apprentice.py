import os
import sys

import click
from app import create_app, db
from app.models import User

app = create_app(os.getenv("FLASK_CONFIG") or "default")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    """Runs the unit tests.

    Args:
        test_names: If provided, runs specific tests by name.
    """
    import unittest

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("tests")

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    sys.exit(not result.wasSuccessful())


# It's recommended to not put `app.run()` here for larger applications
# and instead use `flask run` after setting the FLASK_APP env var
