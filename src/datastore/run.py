from logging.config import dictConfig
from flask import Flask


# Configure App logger
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def createApp(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from .app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .model import db
    db.init_app(app)

    return app


def startApp():
    app = createApp("datastore.config")
    app.run(debug=True)


if __name__ == "__main__":
    startApp()
