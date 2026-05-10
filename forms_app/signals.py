import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TreatmentRequest


def _send_in_background(instance_pk):
    """Run send_to_receiver in a daemon thread so it never blocks the request."""
    from .models import TreatmentRequest
    from .utils import send_to_receiver
    try:
        obj = TreatmentRequest.objects.get(pk=instance_pk)
        if not obj.is_sent:
            send_to_receiver(obj)
    except Exception:
        pass  # Already logged inside send_to_receiver


@receiver(post_save, sender=TreatmentRequest)
def push_to_meeda_on_save(sender, instance, created, **kwargs):
    """
    Every time a TreatmentRequest is saved and not yet sent,
    fire off a background thread to push it to the meeda project.
    """
    if not instance.is_sent:
        t = threading.Thread(
            target=_send_in_background,
            args=(instance.pk,),
            daemon=True,
        )
        t.start()
