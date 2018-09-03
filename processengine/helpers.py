from datetime import datetime
import requests
from django.conf import settings
import json
import time
from django_rq import get_queue, get_worker


def slack_notification(message,
                       channel,
                       username,
                       emoji=":ghost:",
                       title=None,
                       task_id=None):
    """
    Helper function to send notifications to slack
    """
    if title:
        message = "*{}*\n{}".format(title, message)
    if task_id:
        message += "/nFailed task ID: *{}*".format(task_id)
    str_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message += "\n" + str_time
    data = {
        "text": message,
        "channel": channel,
        "link_names": 1,
        "username": username,
        "icon_emoji": emoji,
    }
    requests.post(settings.SLACK_WEBHOOK, data=json.dumps(data))


def retry_handler(job, *exc_info):
    TASK_EXC = {
        # other
        'api.tests.test_exceptions.throw_exception': [
            TypeError,
        ],
    }
    if job.func_name in TASK_EXC and exc_info[0] in TASK_EXC[job.func_name]:
        job.meta.setdefault('failures', 1)
        job.meta['failures'] += 1
        if job.meta['failures'] > settings.QUICKBASE_MAX_RETRIES:
            time.sleep(settings.QUICKBASE_RETRY_INTERVAL)
            worker = get_worker(job.origin)
            worker.move_to_failed_queue(job, *exc_info)
            return True
        for queue in settings.RQ_QUEUES:
            if queue == job.origin:
                queue = get_queue(queue)
                queue.enqueue_job(job)
                return False
        return True
    worker = get_worker(job.origin)
    worker.move_to_failed_queue(job, *exc_info)
    return True
