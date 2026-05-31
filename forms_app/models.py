from django.db import models


class ServiceType(models.TextChoices):
    EXTRACTION = 'خلع', 'خلع'
    ROOT_CANAL = 'استئصال عصب', 'الجلسة الأولى من استئصال العصب'


class TreatmentRequest(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='الاسم بالكامل')
    phone = models.CharField(max_length=10, verbose_name='رقم الجوال')
    id_number = models.CharField(max_length=20, verbose_name='رقم الإثبات')
    birth_date = models.DateField(verbose_name='تاريخ الميلاد')
    nationality = models.CharField(max_length=100, verbose_name='الجنسية')
    city = models.CharField(max_length=100, blank=True, default='', verbose_name='المدينة')
    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
        verbose_name='نوع الخدمة المطلوبة'
    )
    notes = models.TextField(blank=True, verbose_name='ملاحظات إضافية')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التسجيل')
    is_sent = models.BooleanField(default=False, verbose_name='تم الإرسال للمشروع الآخر')

    class Meta:
        verbose_name = 'طلب علاج'
        verbose_name_plural = 'طلبات العلاج'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.phone}"


class WebAppointment(models.Model):
    full_name        = models.CharField(max_length=255, verbose_name='الاسم')
    phone            = models.CharField(max_length=10, verbose_name='رقم الجوال')
    department       = models.CharField(max_length=100, verbose_name='التخصص')
    doctor_id        = models.IntegerField(verbose_name='رقم الطبيب')
    doctor_name      = models.CharField(max_length=255, verbose_name='اسم الطبيب')
    appointment_day  = models.CharField(max_length=10, verbose_name='اليوم')
    appointment_date = models.DateField(verbose_name='التاريخ')
    appointment_time = models.TimeField(verbose_name='الوقت')
    notes            = models.TextField(blank=True, default='', verbose_name='ملاحظات')
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name='وقت الحجز')
    is_sent          = models.BooleanField(default=False, verbose_name='تم الإرسال لميدة')

    class Meta:
        verbose_name = 'حجز موعد'
        verbose_name_plural = 'حجوزات المواعيد'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.doctor_name} - {self.appointment_date}"
