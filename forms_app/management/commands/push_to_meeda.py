from django.core.management.base import BaseCommand
from django.db import connections
from forms_app.models import TreatmentRequest


def push_one(obj, cursor):
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
        obj.full_name, obj.phone, obj.id_number,
        obj.birth_date, obj.nationality, obj.city,
        obj.service_type, obj.notes, obj.created_at,
        obj.pk,
    ])


class Command(BaseCommand):
    help = 'Push unsent TreatmentRequests directly into meeda database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all', action='store_true',
            help='Re-push ALL records (resets is_sent first)',
        )

    def handle(self, *args, **options):
        if options['all']:
            TreatmentRequest.objects.update(is_sent=False)

        qs = TreatmentRequest.objects.filter(is_sent=False).order_by('created_at')
        total   = qs.count()
        success = 0
        failed  = 0

        self.stdout.write(f'Found {total} records to push...')

        conn = connections['meeda']
        with conn.cursor() as cursor:
            for obj in qs:
                try:
                    push_one(obj, cursor)
                    conn.commit()
                    TreatmentRequest.objects.filter(pk=obj.pk).update(is_sent=True)
                    success += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ #{obj.pk} {obj.full_name}'))
                except Exception as e:
                    conn.rollback()
                    failed += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ #{obj.pk} {obj.full_name} — {e}'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done — pushed: {success}  failed: {failed}'))
