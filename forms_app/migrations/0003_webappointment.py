from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_app', '0002_alter_city_alter_service_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='الاسم')),
                ('phone', models.CharField(max_length=10, verbose_name='رقم الجوال')),
                ('department', models.CharField(max_length=100, verbose_name='التخصص')),
                ('doctor_id', models.IntegerField(verbose_name='رقم الطبيب')),
                ('doctor_name', models.CharField(max_length=255, verbose_name='اسم الطبيب')),
                ('appointment_day', models.CharField(max_length=10, verbose_name='اليوم')),
                ('appointment_date', models.DateField(verbose_name='التاريخ')),
                ('appointment_time', models.TimeField(verbose_name='الوقت')),
                ('notes', models.TextField(blank=True, default='', verbose_name='ملاحظات')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='وقت الحجز')),
                ('is_sent', models.BooleanField(default=False, verbose_name='تم الإرسال لميدة')),
            ],
            options={
                'verbose_name': 'حجز موعد',
                'verbose_name_plural': 'حجوزات المواعيد',
                'ordering': ['-created_at'],
            },
        ),
    ]
