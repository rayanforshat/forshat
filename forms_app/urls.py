from django.urls import path
from . import views

app_name = 'forms_app'

urlpatterns = [
    path('مبادرة-العلاج/', views.initiative, name='initiative'),
    path('مبادرة-العلاج/تم-التسجيل/', views.success, name='success'),
]
