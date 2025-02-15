from flask import make_response, redirect, request, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from lib.security.handshake import handshake_required
from lib.user_interactions.email import send_security_code_email
from lib.user_interactions.auth_session import redis_sessions_auth
from lib.app_conf import limiter

@handshake_required
@limiter.limit("5 per hour")
def sign_user_in():
    """Need to grab all user values // transfer from redis_auth"""
    data = request.get_json()
    email = f'email:{data["email"]}'
    pwd_hash = redis_sessions_auth.hget(email, "password")
    
    if pwd_hash is not None and check_password_hash(pwd_hash, data["password"]):
        session["user_auth"] = True
        session["user_key"] = f"email:{email}"

@handshake_required
@limiter.limit("50 per hour")
def register_user():
    data = request.get_json()
    session["no_auth_email"] = data["email"]
    session["no_auth_pswd_hash"] = generate_password_hash(data["password"])
    response = send_security_code_email(session["no_auth_email"])
    if response is not None:
        return jsonify({"status": "success"}), 204
    return jsonify({"status": "error"}), 400

def logout():

    response = make_response(redirect(url_for('home')))
    response.delete_cookie('requested_values_set')
    session.clear()
    
    return redirect(url_for('home'))