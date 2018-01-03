=====
Process Engine
=====

Process Engine is used in conjunction with celery to create async process from
celery tasks via an API


Quick start
-----------

1. Add "processengine" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'processengine',
    ]

2. Include the polls URLconf in your project urls.py like this::

    from processengine.api import router as process_router
    ...

    urlpatterns = [
        url(r'^processengine/', include(process_router.urls)),
        ...
    ]


3. Add the PROCESS_MAP settings with your processes and the tasks to run like
so::

    PROCESS_MAP = {
        'my.process': [
            'path.to.taskfile.task',
        ],
        ...
    }


4. Run `python manage.py migrate` to create the processengine models.

5. to create a process run a POST to http://127.0.0.1:8000/processengine/process/
with the following data::

    data = {
        name: "my.process", # This is the name of your process set in PROCESS_MAP variable
        context: {
            "name": "value" # This is the data that you pass through to your task
        }
    }

Note: Your tasks need to conform to the pattern of json in and json out
