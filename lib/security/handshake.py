from flask import request, session, jsonify
from functools import wraps

def handshake_required(func):
    """Decorator to enforce UUID & CSRF token validation on API requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        client_uuid = request.headers.get("X-Client-UUID")
        csrf_token = request.headers.get("X-CSRF-Token")
        if client_uuid != session.get("client_uuid"):
            return jsonify({"status": "error", "message": "Invalid UUID"}), 403
        if csrf_token != session.get("csrf_token"):
            return jsonify({"status": "error", "message": "CSRF token mismatch"}), 403

        return func(*args, **kwargs)
    
    return decorated_function