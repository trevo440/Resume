from flask import session
import redis, json
redis_sessions_auth = redis.StrictRedis(host="redis", port=6379, db=1)

# ACCOUNT HANDLING
def session_setter(mapping, data):

    if session["user_auth"]:
        if isinstance(data, dict):
            data = json.dumps(data)
        if isinstance(data, bool):
            data = int(data)
        redis_sessions_auth.hset(session["user_key"], mapping, data)
    else:
        session[mapping] = data

def session_getter(mapping):
    if session["user_auth"]:
        data = redis_sessions_auth.hget(session["user_key"], mapping).decode('utf-8')
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass
        return data
    else:
        return session.get(mapping)