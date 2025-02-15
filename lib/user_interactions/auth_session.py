import redis
redis_sessions_auth = redis.StrictRedis(host="redis", port=6379, db=1)