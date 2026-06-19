import logging
import os
from datetime import timedelta
from rq_scheduler import Scheduler
from backend.app.worker.queue import get_redis_conn

logger = logging.getLogger(__name__)


def schedule_recurring_enqueue(function_path: str, cron_seconds: int = 60):
    """Schedule a recurring job that enqueues `function_path` every cron_seconds.

    The worker task will be executed by RQ workers. `function_path` can be a
    callable path (e.g. 'backend.app.worker.tasks.crawl_job').
    """
    conn = get_redis_conn()
    scheduler = Scheduler(connection=conn)
    # Avoid duplicate scheduled jobs by id
    job_id = f'schedule:{function_path}'
    # schedule to run every cron_seconds
    scheduler.schedule(
        scheduled_time=Scheduler.delayed_time(timedelta(seconds=0)),
        func=function_path,
        args=([],),
        interval=cron_seconds,
        repeat=None,
        id=job_id,
    )
    logger.info('Scheduled %s every %s seconds', function_path, cron_seconds)


if __name__ == '__main__':
    fn = os.getenv('SCHEDULE_FUNC', 'backend.app.worker.tasks.crawl_job')
    secs = int(os.getenv('SCHEDULE_INTERVAL', '60'))
    schedule_recurring_enqueue(fn, secs)
