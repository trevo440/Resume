from flask import session
import redis
redis_sessions_auth = redis.StrictRedis(host="redis", port=6379, db=1)

# ACCOUNT HANDLING
def session_setter(mapping, data):
    if session["user_auth"]:
        redis_sessions_auth.hset(session["user_key"], mapping, data)
    else:
        session[mapping] = data

def session_getter(mapping):
    if session["user_auth"]:
        return redis_sessions_auth.hget(session["user_key"], mapping)
    else:
        return session.get(mapping)