import os
import click

from flask import Flask, render_template

from .chat import chat
from .auth import auth
from .config import config

from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError


db = SQLAlchemy()
csrf = CSRFProtect()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_errors(app)
    register_command(app)

    return app


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(chat)


def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_errors(app):
    @app.errorhandle(400)
    def bad_request(e):
        return render_template('error.html', description=e.description, code=e.code), 400

    @app.errorhandle(404)
    def page_not_found(e):
        return render_template('error.html', description=e.description, code=e.code), 404

    @app.errorhandle(500)
    def internal_server_error(e):
        return render_template('error.html', description='internal server error', code='500'), 500

    @app.errorhandle(CSRFError)
    def handle_csrf_error(e):
        return render_template('error.html', description=e.description, code=e.code), 400


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        if drop:
            click.confirm('This option will delete the database, do you want to continue?',
                          abort=True)
            db.drop_all()
            click.echo('Drop database.')
        db.create_all()
        click.echo('Initialized database.')


