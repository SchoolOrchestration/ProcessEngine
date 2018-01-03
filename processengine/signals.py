from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Process


@receiver(post_save, sender=Process, dispatch_uid="api.signals.process_created")
def process_created(sender, instance, created, **kwargs):
    if created:
        instance.run()
