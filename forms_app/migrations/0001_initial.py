from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='الاسم بالكامل')),
                ('phone', models.CharField(max_length=10, verbose_name='رقم الجوال')),
                ('id_number', models.CharField(max_length=20, verbose_name='رقم الإثبات')),
                ('birth_date', models.DateField(verbose_name='تاريخ الميلاد')),
                ('nationality', models.CharField(max_length=100, verbose_name='الجنسية')),
                ('city', models.CharField(max_length=100, verbose_name='المدينة')),
                ('service_type', models.CharField(
                    choices=[('خلع', 'خلع'), ('سحب عصب', 'سحب عصب'), ('جراحة', 'جراحة')],
                    max_length=20,
                    verbose_name='نوع الخدمة المطلوبة',
                )),
                ('notes', models.TextField(blank=True, verbose_name='ملاحظات إضافية')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التسجيل')),
                ('is_sent', models.BooleanField(default=False, verbose_name='تم الإرسال للمشروع الآخر')),
            ],
            options={
                'verbose_name': 'طلب علاج',
                'verbose_name_plural': 'طلبات العلاج',
                'ordering': ['-created_at'],
            },
        ),
    ]
