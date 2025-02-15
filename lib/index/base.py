from flask import render_template, session
from lib.user_interactions.auth_session import session_getter

def home():
    return render_template(
        'home.html',
        res=session.get('resume_sections'),
        cur=session.get('job_description'),
        client_uuid=session["client_uuid"], 
        csrf_token=session["csrf_token"],
        user_auth=session["user_auth"],
        user_email=session.get("user_key", "").replace("email:", ""),
    )

def get_started():
    return render_template(
        'set_all_data.html',
        client_uuid=session["client_uuid"], 
        csrf_token=session["csrf_token"],
        user_auth=session["user_auth"],
        user_email=session.get("user_key", "").replace("email:", ""),
    )
