import os
import redis


redis_url = os.getenv('REDISTOGO_URL')
conn = redis.from_url(redis_url, max_connections=80)