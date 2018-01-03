from celery import shared_task


@shared_task
def ping(*args, **kwargs):
    return 'pong'
