from flask import Flask, send_from_directory
from stegano import auth, api
from stegano.extensions import db, jwt, migrate
from .helpers import loadconf, get_save_location
import os


def create_app(config=None, testing=False, cli=False):
    '''Application factory, used to create application
    '''
    app = Flask('STEGANO')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)

    @app.route('/assets/images/<img_file>', methods=['GET'])
    def serveimg(img_file):
        imgpath = get_save_location(img_file)
        dirc = os.path.dirname(imgpath)
        return send_from_directory(dirc, img_file, as_attachment=True)
    return app


def configure_app(app, testing=False):
    '''set configuration for application
    '''
    # default configuration
    env_conf = loadconf()
    app.config.from_object(env_conf)

    if testing is True:
        # override with testing config
        app.config.from_object('stegano.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar(
            'STEGANO_ENV', silent=True)


def configure_extensions(app, cli):
    '''configure flask extensions
    '''
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    '''register all blueprints for application
    '''
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
