import threading
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TreatmentRequest, WebAppointment

logger = logging.getLogger(__name__)


def _push_to_meeda(instance_pk):
    """
    كتابة مباشرة في قاعدة بيانات ميدة — بدون HTTP.
    يعمل في thread منفصل حتى لا يبطّئ الطلب.
    """
    from django.db import connections
    try:
        obj = TreatmentRequest.objects.get(pk=instance_pk)
        if obj.is_sent:
            return

        conn = connections['meeda']
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO initiative_treatmentrequest
                    (full_name, phone, id_number, birth_date, nationality,
                     city, service_type, notes, created_at, received_at,
                     source_id, status, handled_by_id, handled_at)
                VALUES
                    (%s, %s, %s, %s, %s,
                     %s, %s, %s, %s, NOW(),
                     %s, 'pending', NULL, NULL)
                ON CONFLICT (source_id) DO NOTHING
            """, [
                obj.full_name,
                obj.phone,
                obj.id_number,
                obj.birth_date,
                obj.nationality,
                obj.city,
                obj.service_type,
                obj.notes,
                obj.created_at,
                obj.pk,          # source_id
            ])
            conn.commit()

        # علّم السجل كـ مُرسَل
        TreatmentRequest.objects.filter(pk=instance_pk).update(is_sent=True)
        logger.info(f'TreatmentRequest #{instance_pk} pushed to meeda directly.')

    except Exception as e:
        logger.error(f'Failed to push TreatmentRequest #{instance_pk} to meeda: {e}')


@receiver(post_save, sender=TreatmentRequest)
def push_to_meeda_on_save(sender, instance, created, **kwargs):
    """يُشغَّل عند كل حفظ جديد غير مُرسَل."""
    if not instance.is_sent:
        t = threading.Thread(
            target=_push_to_meeda,
            args=(instance.pk,),
            daemon=True,
        )
        t.start()


def _push_appointment_to_meeda(instance_pk):
    from django.db import connections
    try:
        obj = WebAppointment.objects.get(pk=instance_pk)
        if obj.is_sent:
            return

        conn = connections['meeda']
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO initiative_webappointment
                    (full_name, phone, department, doctor_id, doctor_name_cached,
                     appointment_day, appointment_date, appointment_time,
                     notes, status, created_at)
                VALUES
                    (%s, %s, %s, %s, %s,
                     %s, %s, %s,
                     %s, 'pending', NOW())
                ON CONFLICT DO NOTHING
            """, [
                obj.full_name,
                obj.phone,
                obj.department,
                obj.doctor_id,
                obj.doctor_name,
                obj.appointment_day,
                obj.appointment_date,
                obj.appointment_time,
                obj.notes,
            ])
            conn.commit()

        WebAppointment.objects.filter(pk=instance_pk).update(is_sent=True)
        logger.info(f'WebAppointment #{instance_pk} pushed to meeda.')

    except Exception as e:
        logger.error(f'Failed to push WebAppointment #{instance_pk} to meeda: {e}')


@receiver(post_save, sender=WebAppointment)
def push_appointment_to_meeda(sender, instance, created, **kwargs):
    if created and not instance.is_sent:
        t = threading.Thread(
            target=_push_appointment_to_meeda,
            args=(instance.pk,),
            daemon=True,
        )
        t.start()
