import os
from redis import Redis
from rq import Queue

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

def get_redis_conn() -> Redis:
    return Redis.from_url(REDIS_URL)


def get_queue(name: str = 'crawler') -> Queue:
    conn = get_redis_conn()
    return Queue(name, connection=conn)
