# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase, override_settings
from processengine.models import Process
from .datas import PROCESS_MAP
from .makers import create_fake_process

import processengine.models
import json, unittest


@override_settings(PROCESS_MAP=PROCESS_MAP)
@override_settings(CELERY_ALWAYS_EAGER=True)
class CreateProcessTestCase(TestCase):

    def setUp(self):
        url = reverse('process-list')

        setattr(processengine.models, 'PROCESS_NAMES', PROCESS_MAP)
        data = {
            'name': 'foo.bar'
        }
        self.result = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )

    @unittest.skip("Can't work out how to set choices properly")
    def test_create_process_ok(self):
        import pdb; pdb.set_trace()
        assert self.result.status_code == 201

    @unittest.skip("Can't work out how to set choices properly")
    def test_creates_process(self):
        assert Process.objects.count() == 1

    @unittest.skip("Can't work out how to set choices properly")
    def test_process_complete(self):
        assert Process.objects.filter(id=self.result.json()['id']).status == 'C'


class ProcessListEndpointTestCase(TestCase):

    def setUp(self):
        url = reverse('process-list')
        [create_fake_process() for p in range(0, 5)]
        self.result = self.client.get(url)

    def test_is_ok(self):
        assert self.result.status_code == 200

    def test_returns_correct_number_of_results(self):
        assert len(self.result.json().get('results')) == 5
