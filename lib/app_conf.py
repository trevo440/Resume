from flask import Flask
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from lib.security.middleware import check_session_data

import redis

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True 
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'kwip:'
app.config['SESSION_REDIS'] = redis.StrictRedis(host="redis", port=6379, db=0)
app.config['RATELIMIT_STORAGE_URI'] = redis.StrictRedis(host="redis", port=6379, db=2)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
"""
def dynamic_rate_limit():
    # setup later for when we have paid users
    user_id = session.get("user_id")  # Assuming user_id is stored in session
    if not user_id:
        return "5 per minute"  # Default limit for non-authenticated users
    
    try:
        user = User.query.filter_by(id=user_id).one()
        if user.account_type == "paid":
            return "100 per minute"  # Higher limit for paid users
        else:
            return "5 per minute"  # Lower limit for free users
    except NoResultFound:
        return "5 per minute"  # Default limit if user not found
"""

Session(app)
app.secret_key = 'your_secret_key'
app.before_request(check_session_data)
# app.after_request(lambda response: response.headers.update({"X-Content-Type-Options": "nosniff"}))

limiter = Limiter(
    key_func=get_remote_address, 
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['RATELIMIT_STORAGE_URI']
)