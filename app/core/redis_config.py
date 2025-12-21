from redis import StrictRedis

r = StrictRedis(host="localhost", port=6379, encoding="utf-8", decode_responses=True)
MAX_AGE = 3600