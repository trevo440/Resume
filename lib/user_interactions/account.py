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
    
    if pwd_hash is not None and check_password_hash(pwd_hash.decode('utf-8'), data["password"]):
        session["user_auth"] = True
        session["user_key"] = email
        return jsonify({"status": "success"}), 200
 
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@handshake_required
@limiter.limit("50 per hour")
def register_user():
    """
    1. Receive email and password from the client
    2. Check if the email is already registered in Redis
    3. If not, generate the temporary password hash
    4. Send the security code email to the user
    5. Store the email (key) and password hash in Redis
    """
    data = request.get_json()
    session["no_auth_email"] = data["email"]
    if redis_sessions_auth.exists(f'email:{data["email"]}'):
        return jsonify({"status": 409, "message": "Email already registered"}), 409
    
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