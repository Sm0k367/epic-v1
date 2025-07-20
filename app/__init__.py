from flask import Flask
from config import Config
import os

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)

    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()

    # Register Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
