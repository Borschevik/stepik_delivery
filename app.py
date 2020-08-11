# pylint: disable=W0621,W0622,W0613
"""Flask app"""
from flask import Flask, Response, redirect
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

from config.config import config
from config.extenstions import db, migrate


def add_cli_commands(app: Flask):
    """
    Add cli commands for flask servie

    :param app:
    """
    # pylint: disable=C0415
    from cli.commands.cli_create_db import db_tasks

    app.cli.add_command(db_tasks)


def register_blueprints(app):
    """
    Add blueprints to project

    :param app:
    """
    # pylint: disable=C0415
    from views.views import service

    app.register_blueprint(service)


def jinja_extensions(app: Flask):
    """
    Add new jinja filters

    :param app:
    """
    # pylint: disable=C0415
    app.jinja_env.add_extension("jinja2.ext.do")


def register_extensions(app: Flask):
    """
    Register extensions for application
    """
    db.init_app(app)
    with app.app_context():
        migrate.init_app(app, db, directory=app.config["MIGRATION_DIR"])


def create_app() -> Flask:
    """
    App facrtory
    """
    app: Flask = Flask(__name__)
    app.config.from_object(config)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    add_cli_commands(app)
    register_blueprints(app)
    jinja_extensions(app)
    register_extensions(app)

    return app


def add_admin(app: Flask, basic_auth: BasicAuth):
    """
    Add admin

    :param app:
    """
    # pylint: disable=C0415, R0201, R1720, C0116
    from database.models import Category, Order, Meal, User

    class AuthException(HTTPException):
        """
        Atuh exception
        """

        def __init__(self, message):
            super().__init__(
                message,
                Response(
                    "You could not be authenticated. Please refresh the page.",
                    401,
                    {"WWW-Authenticate": 'Basic realm="Login Required"'},
                ),
            )

    class MyModelView(ModelView):
        """
        Custom model setting
        """

        def is_accessible(self):
            if not basic_auth.authenticate():
                return AuthException("Не авторизированы")
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())

    class MyAdminIndexView(AdminIndexView):
        """
        Custom Admin Index view
        """

        def is_accessible(self):
            if not basic_auth.authenticate():
                raise AuthException("Not authenticated.")
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())

    admin = Admin(
        app,
        index_view=MyAdminIndexView(),
        name="Admin Panel",
        template_mode="bootstrap3",
    )
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Order, db.session))
    admin.add_view(MyModelView(Category, db.session))
    admin.add_view(MyModelView(Meal, db.session))


app: Flask = create_app()
basic_auth: BasicAuth = BasicAuth(app)
add_admin(app, basic_auth)

if __name__ == "__main__":
    app.run()
