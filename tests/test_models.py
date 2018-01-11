# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, override_settings

from processengine.models import Process
from unittest.mock import patch

from .datas import PROCESS_MAP


@override_settings(PROCESS_MAP=PROCESS_MAP)
@override_settings(CELERY_ALWAYS_EAGER=True)
class ProcessModelTestCase(TestCase):

    def setUp(self):

        process = Process()
        process.name = 'foo.bar'
        process.context = {'foo': 'bar'}
        process.save()

        self.process = process

    def test_run(self):
        self.process.run()
        assert len(self.process.task_ids) == 1

    @patch.object(Process, 'run')
    def test_it_calls_instance_run_on_creation(self, mock_process_run):

        process = Process()
        process.name = 'foo.bar'
        process.save()
        assert mock_process_run.call_count == 1

    @patch('processengine.tasks.ping.delay')
    def test_calls_correct_method(self, mock_ping):
        self.process.run()
        assert mock_ping.called
