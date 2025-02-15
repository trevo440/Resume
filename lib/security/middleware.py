from flask import session, redirect, url_for, request
import os, uuid
from lib.user_interactions.auth_session import redis_sessions_auth

def check_session_data():
    
    if "user_auth" not in session:
        session["user_auth"] = False

    if "user_email" not in session:
        session["user_email"] = str(uuid.uuid4())

    if "client_uuid" not in session:
        session["client_uuid"] = str(uuid.uuid4())

    if "csrf_token" not in session:
        session["csrf_token"] = os.urandom(32).hex()

    if not session["user_auth"]:
        if "resume_provided" not in session:
            session["resume_provided"] = False
    
    if session["user_auth"]:
        resume_provided = redis_sessions_auth.hget(session["user_key"], "resume_provided") 
        if resume_provided is None or resume_provided == "False":
            redis_sessions_auth.hset(session["user_key"], "resume_provided", "False")
            session['resume_provided'] = False
        else:
            session["resume_provided"] = True

    if not session["resume_provided"] and request.endpoint not in [
        'static', 
        'set_job_description', 
        'set_resume_sections',
        'get_started',
        'download_pdf',
        'view_example',
        'register_user',
        'sign_user_in',
        'validate_verification_email',
    ]:
        return redirect(url_for('get_started'))