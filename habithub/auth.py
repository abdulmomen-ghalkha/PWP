from functools import wraps
from flask import request
from werkzeug.exceptions import Unauthorized

API_KEY = "aleem"

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            raise Unauthorized(description="Invalid or API key not found")
        return f(*args, **kwargs)
    return decorated
