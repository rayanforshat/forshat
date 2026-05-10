from django.core.management.base import BaseCommand
from forms_app.models import TreatmentRequest
from forms_app.utils import send_to_receiver


class Command(BaseCommand):
    help = 'Push all unsent TreatmentRequest records to the meeda initiative API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Re-send ALL records, including already-sent ones',
        )

    def handle(self, *args, **options):
        if options['all']:
            qs = TreatmentRequest.objects.all()
            # Reset is_sent so send_to_receiver will update it
            qs.update(is_sent=False)
        else:
            qs = TreatmentRequest.objects.filter(is_sent=False)

        total   = qs.count()
        success = 0
        failed  = 0

        self.stdout.write(f'Found {total} records to send...')

        for req in qs.order_by('created_at'):
            ok = send_to_receiver(req)
            if ok:
                success += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ #{req.pk} {req.full_name}'))
            else:
                failed += 1
                self.stdout.write(self.style.ERROR(f'  ✗ #{req.pk} {req.full_name}'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done — sent: {success}  failed: {failed}'))
