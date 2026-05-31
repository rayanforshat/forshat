from django.core.management.base import BaseCommand
from django.db import connections
from forms_app.models import WebAppointment


def push_one(obj, cursor):
    cursor.execute("""
        INSERT INTO initiative_webappointment
            (full_name, phone, department, doctor_id, doctor_name_cached,
             appointment_day, appointment_date, appointment_time,
             notes, status, created_at)
        VALUES
            (%s, %s, %s, %s, %s,
             %s, %s, %s,
             %s, 'pending', NOW())
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


class Command(BaseCommand):
    help = 'Push unsent WebAppointments directly into meeda database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all', action='store_true',
            help='Re-push ALL records (resets is_sent first)',
        )

    def handle(self, *args, **options):
        if options['all']:
            WebAppointment.objects.update(is_sent=False)

        qs = WebAppointment.objects.filter(is_sent=False).order_by('created_at')
        total = qs.count()
        success = 0
        failed = 0

        self.stdout.write(f'Found {total} unsent appointments to push...')

        conn = connections['meeda']
        with conn.cursor() as cursor:
            for obj in qs:
                try:
                    push_one(obj, cursor)
                    conn.commit()
                    WebAppointment.objects.filter(pk=obj.pk).update(is_sent=True)
                    success += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ #{obj.pk} {obj.full_name} — {obj.appointment_date} {obj.appointment_time}'))
                except Exception as e:
                    conn.rollback()
                    failed += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ #{obj.pk} {obj.full_name} — {e}'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done — pushed: {success}  failed: {failed}'))
