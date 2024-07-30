## DefaultImports
import hashlib
import os
import datetime
import logging
import secrets

## LibsImports
from flask import Flask, jsonify, request, make_response
from flask_basicauth import BasicAuth
from werkzeug.urls import unquote
from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger
import supabase

## LocalImports
from apis.psicologos import psicologos
from apis.admnistrador import admnistrador
from apis.auth import auth

def config_logger():
    logging.basicConfig(filename='error.log', level=logging.ERROR)

    logger = logging.getLogger(__name__)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def setup_app():
    app = Flask(__name__)
    CORS(app)
    swagger = Swagger(app)
    app.register_blueprint(psicologos)
    app.register_blueprint(admnistrador)
    app.register_blueprint(auth)
    return app

if __name__ == '__main__':
    config_logger()
    app = setup_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
