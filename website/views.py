from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def home(request):
    """الصفحة الرئيسية"""
    return render(request, 'website/home.html')


def services(request):
    """صفحة الخدمات والعروض"""
    # البيانات ثابتة في HTML، لا حاجة لتمرير context معقد
    context = {
        'total_count': 15,  # عدد الخدمات المعروضة
    }
    
    return render(request, 'website/services.html', context)