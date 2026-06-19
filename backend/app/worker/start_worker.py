"""Run an RQ worker programmatically. Useful for containerized deployments.

Usage: python -m backend.app.worker.start_worker
"""
import logging
import os
from rq import Worker, Connection
from backend.app.worker.queue import get_redis_conn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_worker(queues=('crawler',)):
    redis_conn = get_redis_conn()
    with Connection(redis_conn):
        worker = Worker(list(queues))
        logger.info('Starting RQ worker for queues: %s', queues)
        worker.work()


if __name__ == '__main__':
    qnames = os.getenv('RQ_QUEUES', 'crawler').split(',')
    run_worker(qnames)
