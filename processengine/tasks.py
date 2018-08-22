from django_rq import job
from django.conf import settings

@job(settings.RQ_DEFAULT_QUEUE)
def ping(*args, **kwargs):
    return 'pong'
