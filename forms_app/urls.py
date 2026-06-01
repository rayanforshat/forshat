from django.urls import path
from . import views

app_name = 'forms_app'

urlpatterns = [
    path('مبادرة-العلاج/', views.initiative, name='initiative'),
    path('مبادرة-العلاج/تم-التسجيل/', views.success, name='success'),
    path('حجز-موعد/', views.booking, name='booking'),
    path('حجز-موعد/تأكيد/', views.submit_booking, name='submit_booking'),
    path('حجز-موعد/تحقق-جوال/', views.check_phone, name='check_phone'),
]
