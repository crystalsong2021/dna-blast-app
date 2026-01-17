from flask import Flask
from .routes import bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(bp)

    return app

