from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .offers_data import build_services_context


def home(request):
    """الصفحة الرئيسية"""
    return render(request, 'website/home.html')


def services(request):
    """صفحة الخدمات والعروض — تُعرض من العروض المنشورة في نظام ميدا."""
    context = build_services_context()
    context['active_category'] = request.GET.get('category', 'all')
    context['search_query'] = request.GET.get('search', '')
    context['sort_by'] = request.GET.get('sort', 'default')
    return render(request, 'website/services.html', context)