from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils.module_loading import import_string
from django.conf import settings
import json


PROCESS_NAMES = [(key,key) for key, value in settings.PROCESS_MAP.items()]


class Process(models.Model):
    """
    # create new process
    POST /process/ --data={name: 'foo.bar', context: { ... }}

    # get process status:
    GET /process/:id/
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, db_index=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    context = JSONField(default={}, blank=True, null=True)
    task_ids = ArrayField(models.CharField(max_length=100), blank=True, null=True, db_index=True)

    @property
    def triggers(self):
        return settings.PROCESS_MAP.get(self.name, [])

    @property
    def status(self):
        """Failed/Successful/Pending"""
        pass

    def run(self):
        task_ids = []
        for trigger in self.triggers:
            task_to_run = import_string(trigger)
            task = task_to_run.delay(self.context)
            task_ids.append(task.id)
        self.task_ids = task_ids
        self.save()


from .signals import *
