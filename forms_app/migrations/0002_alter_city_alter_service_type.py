from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatmentrequest',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='المدينة'),
        ),
        migrations.AlterField(
            model_name='treatmentrequest',
            name='service_type',
            field=models.CharField(
                choices=[('خلع', 'خلع'), ('استئصال عصب', 'الجلسة الأولى من استئصال العصب')],
                max_length=20,
                verbose_name='نوع الخدمة المطلوبة',
            ),
        ),
    ]
