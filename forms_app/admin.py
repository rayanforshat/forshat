from django.contrib import admin
from .models import TreatmentRequest


@admin.register(TreatmentRequest)
class TreatmentRequestAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'phone', 'id_number',
        'nationality', 'city', 'service_type',
        'created_at', 'is_sent',
    )
    list_filter = ('service_type', 'city', 'nationality', 'is_sent', 'created_at')
    search_fields = ('full_name', 'phone', 'id_number', 'city', 'nationality')
    readonly_fields = ('created_at', 'is_sent')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('البيانات الشخصية', {
            'fields': ('full_name', 'phone', 'id_number', 'birth_date', 'nationality', 'city')
        }),
        ('تفاصيل الطلب', {
            'fields': ('service_type', 'notes')
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'is_sent'),
            'classes': ('collapse',),
        }),
    )
