import json

import responses
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from processengine.models import Process
from rq import SimpleWorker
from unittest.mock import patch
from django_rq import get_queue
from processengine.helpers import retry_handler

@override_settings(SLACK_WEBHOOK="http://example.com",
                   SLACK_PROCESS_CHANNEL = "#Processes",
                   SLACK_PROCESS_USERNAME = "Someuser",
                   SLACK_PROCESS_EMOJI = ":ghost:",
                   SERVICE_NAME = "Someservice",
                   DEBUG=False)
@override_settings(CELERY_ALWAYS_EAGER = True)
class RunTaskTestCase(TestCase):

    @patch.object(Process, 'run')
    def setUp(self, mock_process):
        self.queue = get_queue(name=settings.RQ_DEFAULT_QUEUE, async=False)
        self.worker = SimpleWorker(
            self.queue,
            connection=self.queue.connection, exception_handlers=[retry_handler])

    @responses.activate
    def test_call_valid_task_no_params(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        # Check that we start with zero Processes
        process_count = Process.objects.count()
        self.assertEqual(process_count, 0)
        # Run the command
        args = ['ping']
        opts = {}
        call_command('run_task', *args, **opts)
        self.worker.work(burst=True)
        # Check that we now have 1 Process created
        process_count = Process.objects.count()

        self.assertEqual(len(responses.calls), 1)
        self.assertIn("Process Creation Succeeded",
                      responses.calls[0].request.body)
        self.assertEqual(process_count, 1)


    @responses.activate
    def test_call_invalid_task_no_params(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        # Check that we start with zero Processes
        process_count = Process.objects.count()
        self.assertEqual(process_count, 0)
        # Run the command
        args = ['Mickey Mouse']
        opts = {}
        call_command('run_task', *args, **opts)
        # Check that we still have 0 Processes
        process_count = Process.objects.count()
        self.assertEqual(len(responses.calls), 1)
        self.assertIn("this task is unknown", responses.calls[0].request.body)
        self.assertEqual(process_count, 0)

    @responses.activate
    def test_call_valid_task_with_params(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        # Check that we start with zero Processes
        process_count = Process.objects.count()
        self.assertEqual(process_count, 0)
        # Run the command
        param1 = json.dumps({'a': "aaaaa"})
        args = ['ping', param1]
        opts = {}
        call_command('run_task', *args, **opts)
        # Check that we now have 1 Process created
        process_count = Process.objects.count()
        self.assertEqual(len(responses.calls), 1)
        self.assertIn("Process Creation Succeeded",
                      responses.calls[0].request.body)
        self.assertEqual(process_count, 1)

    @responses.activate
    def test_call_valid_task_with_non_json_params(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        # Check that we start with zero Processes
        process_count = Process.objects.count()
        self.assertEqual(process_count, 0)
        # Run the command
        param1 = {'a': "aaaaa"}
        args = ['ping', param1]
        opts = {}
        call_command('run_task', *args, **opts)
        # Check that we now have 1 Process created
        process_count = Process.objects.count()
        self.assertEqual(len(responses.calls), 1)
        self.assertIn("don't appear to be valid JSON",
                      responses.calls[0].request.body)
        self.assertEqual(process_count, 0)

    @responses.activate
    def test_call_valid_task_with_non_dict_params(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        # Check that we start with zero Processes
        process_count = Process.objects.count()
        self.assertEqual(process_count, 0)
        # Run the command
        param1 = json.dumps("aaa")
        args = ['ping', param1]
        opts = {}
        call_command('run_task', *args, **opts)
        # Check that we now have 1 Process created
        process_count = Process.objects.count()
        self.assertEqual(len(responses.calls), 1)
        self.assertIn("not a valid dict", responses.calls[0].request.body)
        self.assertEqual(process_count, 0)
