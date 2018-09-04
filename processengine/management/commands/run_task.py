import json
from contextlib import suppress

from django.conf import settings
from django.core.management.base import BaseCommand
from processengine.models import Process

from processengine.helpers import slack_notification

SPACER_LINE = """
===============================================================================
"""


class Command(BaseCommand):
    help = 'Runs a specified task through the process engine.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('task', nargs='+')

    def handle(self, *args, **options):
        """
        Run the specified task through the process engine.
        """
        task_name = options['task'][0]
        slack_channel = settings.SLACK_PROCESS_CHANNEL
        slack_username = settings.SLACK_PROCESS_USERNAME
        slack_emoji = settings.SLACK_PROCESS_EMOJI

        if task_name in settings.PROCESS_MAP:
            param_string = None
            with suppress(IndexError):
                param_string = options['task'][1]
            if param_string:
                try:
                    params = json.loads(param_string)
                except Exception as e:
                    if not settings.DEBUG and settings.SLACK_WEBHOOK:
                        param_string = str(param_string)
                        title = settings.SERVICE_NAME + ": Process Creation Failed"
                        message = (
                            "Arguments for task {} don't appear to be valid"
                            " JSON.\nArguments were {}")
                        message = message.format(task_name, param_string)
                        slack_notification(message=message,
                                           channel=settings.SLACK_PROCESS_CHANNEL,
                                           username=settings.SLACK_PROCESS_USERNAME,
                                           emoji=settings.SLACK_PROCESS_EMOJI,
                                           title=title)
                    else:
                        print(SPACER_LINE)
                        print("Arguments for task {} do not appear to be valid"
                              " JSON.".format(
                                  task_name))
                        print(SPACER_LINE)
                    return
                if not type(params) == dict:
                    if not settings.DEBUG and settings.SLACK_WEBHOOK:
                        title = settings.SERVICE_NAME + ": Process Creation Failed"
                        message = ("Arguments for task {} are not a valid dict"
                                   ".\nArguments were {}")
                        message = message.format(task_name, param_string)
                        slack_notification(message=message,
                                           channel=settings.SLACK_PROCESS_CHANNEL,
                                           username=settings.SLACK_PROCESS_USERNAME,
                                           emoji=settings.SLACK_PROCESS_EMOJI,
                                           title=title)
                    else:
                        print(SPACER_LINE)
                        print("Arguments for task {} do not appear to be a "
                              "JSON dict.".format(task_name))
                        print(SPACER_LINE)
                    return
            process = Process.objects.create(name=task_name, context={})
            message = "Running task '{}' with the following task ids:\n{}"
            message = message.format(task_name, process.task_ids)
            if settings.DEBUG:
                print(SPACER_LINE)
                print(message)
                print(SPACER_LINE)
            elif settings.SLACK_WEBHOOK:
                title = settings.SERVICE_NAME + ": Process Creation Succeeded"
                slack_notification(message=message,
                                   channel=settings.SLACK_PROCESS_CHANNEL,
                                   username=settings.SLACK_PROCESS_USERNAME,
                                   emoji=settings.SLACK_PROCESS_EMOJI,
                                   title=title)
        else:
            if not settings.DEBUG and settings.SLACK_WEBHOOK:
                title = settings.SERVICE_NAME + ": Process Creation Failed"
                message = (
                    "We attempted to create a process running task *'{}'*, "
                    "but this task is unknown.")
                message = message.format(task_name)
                slack_notification(message=message,
                                   channel=settings.SLACK_PROCESS_CHANNEL,
                                   username=settings.SLACK_PROCESS_USERNAME,
                                   emoji=settings.SLACK_PROCESS_EMOJI,
                                   title=title)
            else:
                print(SPACER_LINE)
                print("Couldn't find task '{}'".format(task_name))
                print(SPACER_LINE)
