import responses
from django.test import TestCase, override_settings
from django.conf import settings
from processengine.helpers import slack_notification

@override_settings(SLACK_WEBHOOK="http://example.com",
                   SLACK_PROCESS_CHANNEL = "#Processes",
                   SLACK_PROCESS_USERNAME = "Someuser",
                   SLACK_PROCESS_EMOJI = ":ghost:",
                   SERVICE_NAME = "Someservice",
                   DEBUG=False)

class SlackNotificationTestCase(TestCase):

    def setUp(self):
        self.message = "Test message"
        self.channel = "My Channel"
        self.username = "user123"
        self.emoji=":fish:"
        self.title="Message Title"
        self.task_id="abc123"

    @responses.activate
    def test_bold_title_included_in_message_if_passed(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        slack_notification(message=self.message,
                           channel=self.channel,
                           username=self.username,
                           emoji=self.emoji,
                           title=self.title,
                           task_id=self.task_id)
        bold_title = "*{}*".format(self.title)
        self.assertIn(bold_title, responses.calls[0][0].body)

    @responses.activate
    def test_title_not_included_in_message_if_omitted(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        slack_notification(message=self.message,
                           channel=self.channel,
                           username=self.username,
                           emoji=self.emoji,
                           # No title passed
                           task_id=self.task_id)
        bold_title = "*{}*".format(self.title)
        self.assertNotIn(bold_title, responses.calls[0][0].body)

    @responses.activate
    def test_task_id_included_in_message_if_passed(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        slack_notification(message=self.message,
                           channel=self.channel,
                           username=self.username,
                           emoji=self.emoji,
                           title=self.title,
                           task_id=self.task_id)
        task_id_message = "Failed task ID: *{}*".format(self.task_id)
        self.assertIn(task_id_message, responses.calls[0][0].body)

    @responses.activate
    def test_task_id_not_included_in_message_if_omitted(self):
        responses.add(responses.POST, url=settings.SLACK_WEBHOOK, status=200)
        slack_notification(message=self.message,
                           channel=self.channel,
                           username=self.username,
                           emoji=self.emoji,
                           title=self.title,
                           # no task_id passed
        )
        task_id_message = "Failed task ID: *{}*".format(self.task_id)
        self.assertNotIn(task_id_message, responses.calls[0][0].body)
