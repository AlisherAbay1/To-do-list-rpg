from redis.asyncio import Redis

r = Redis(host="localhost", port=6379, encoding="utf-8", decode_responses=True)
MAX_AGE = 3600