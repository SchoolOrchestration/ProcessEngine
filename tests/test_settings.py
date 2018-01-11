from kombu import Exchange, Queue
import os
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
    "processengine",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}
PROCESS_MAP = {
    'foo.bar': [
        'processengine.tasks.ping',
    ],
}


CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')

BROKER_URL = 'redis://{hostname}/0'.format(hostname=REDIS_HOST)

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10

# Celery configuration

# configure queues, currently we have only one
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

CELERY_IMPORTS = ("processengine.tasks")
# Sensible settings for celery
CELERY_ALWAYS_EAGER = True
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively,
# change it to False
# Or change this setting on tasks level
CELERY_IGNORE_RESULT = False
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 18000

# # Set django as celery result backend
CELERY_RESULT_BACKEND = 'django-db'

# Don't use pickle as serializer, json is much safer
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_CONCURRENCY = 10
CELERYD_PREFETCH_MULTIPLIER = 10
CELERYD_MAX_TASKS_PER_CHILD = 1000
