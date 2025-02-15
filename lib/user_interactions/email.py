from flask import request, session
from datetime import datetime, timedelta, timezone
import sendgrid, uuid
from sendgrid.helpers.mail import Mail, Email, To, Personalization
from lib.security.handshake import handshake_required
from lib.app_conf import limiter
from lib.user_interactions.auth_session import redis_sessions_auth
from lib.user_interactions.roles import ACCOUNT_ROLES

with open("./pswd.txt", "r") as f:
    sendgrid_key = f.read()

def send_security_code_email(recipient_email):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_key)
        security_code = str(uuid.uuid4())[:6]
        session["auth_code"] = security_code
        session["auth_expiry"] = (datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp()

        # Create Mail object with template
        mail = Mail(from_email=Email("sender@kwip.info"))
        mail.template_id = "d-c7258ed1e04e4ddf841581dd12d5b269"

        personalization = Personalization()
        personalization.add_to(To(recipient_email))
        personalization.dynamic_template_data = {
            "CODE": security_code
        }
        mail.add_personalization(personalization)
        response = sg.send(mail)
        return response.status_code

    except Exception:
        return None
    
@handshake_required
@limiter.limit("5 per hour")
def validate_verification_email():
    auth_expiry = session.get("auth_expiry")
    if auth_expiry and (datetime.now(timezone.utc)).timestamp() > auth_expiry:
        session.pop("auth_code", None)
        session.pop("auth_expiry", None)
    

    data = request.get_json()
    if session.get("auth_code") == data["verify-code"]:
        """Need to set all user values // transfer from session"""
        email = session["no_auth_email"]
        session.clear()
        
        session["user_email"] = email
        session["user_key"] = f"email:{email}"
        session["user_auth"] = True

        if not redis_sessions_auth.hget(session["user_key"], "password"):
            redis_sessions_auth.hset(session["user_key"], "password", session["no_auth_pswd_hash"])

        if not redis_sessions_auth.hget(session["user_key"], "role"):
            redis_sessions_auth.hset(session["user_key"], "role", ACCOUNT_ROLES["basic"])

        return "", 204
    return "", 403