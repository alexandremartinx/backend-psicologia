import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
import supabase
from dotenv import load_dotenv
from functools import wraps
from services.auth_guard import auth_guard

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def auth_guard_swag(auth_role, swagger_file):
    def decorator(f):
        @swag_from(os.path.join(BASE_DIR, 'apis/swagger/', swagger_file))
        @auth_guard(auth_role)
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped
    return decorator

def databaseConfig():
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    return supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


db = databaseConfig()