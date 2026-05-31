import re
import json
import urllib.request
from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import TreatmentRequestForm
from .models import WebAppointment

MEEDA_API = 'http://127.0.0.1:8000/initiative'

DAY_AR = {
    'sat': 'السبت', 'sun': 'الأحد', 'mon': 'الاثنين',
    'tue': 'الثلاثاء', 'wed': 'الأربعاء', 'thu': 'الخميس', 'fri': 'الجمعة',
}


def initiative(request):
    if request.method == 'POST':
        form = TreatmentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forms_app:success')
    else:
        form = TreatmentRequestForm()

    return render(request, 'forms_app/initiative.html', {'form': form})


def success(request):
    return render(request, 'forms_app/success.html')


def booking(request):
    from django.conf import settings
    return render(request, 'forms_app/booking.html', {
        'meeda_api_url': settings.MEEDA_API_URL,
    })


def booking_success(request):
    data = request.session.pop('booking_data', None)
    if not data:
        return redirect('forms_app:booking')
    return render(request, 'forms_app/booking_success.html', {'booking': data})


@require_POST
def submit_booking(request):
    try:
        data = json.loads(request.body)
        full_name  = data.get('full_name', '').strip()
        phone      = data.get('phone', '').strip()
        department = data.get('department', '').strip()
        doctor_id  = data.get('doctor_id')
        doctor_name = data.get('doctor_name', '').strip()
        day_code   = data.get('day', '').strip()
        day_date   = data.get('date', '').strip()
        time_str   = data.get('time', '').strip()
        notes      = data.get('notes', '').strip()

        if not all([full_name, phone, department, doctor_id, day_code, day_date, time_str]):
            return JsonResponse({'error': 'بيانات ناقصة'}, status=400)

        if not re.match(r'^5\d{8}$', phone):
            return JsonResponse({'error': 'رقم الجوال يجب أن يبدأ بـ 5 ويتكون من 9 أرقام'}, status=400)

        appt_date = date.fromisoformat(day_date)
        if appt_date <= date.today():
            return JsonResponse({'error': 'لا يمكن حجز موعد في نفس اليوم أو يوم سابق'}, status=400)

        if WebAppointment.objects.filter(doctor_id=doctor_id, appointment_date=appt_date, appointment_time=time_str).exists():
            return JsonResponse({'error': 'هذا الوقت محجوز، يرجى اختيار وقت آخر'}, status=400)

        appt = WebAppointment.objects.create(
            full_name=full_name,
            phone=phone,
            department=department,
            doctor_id=int(doctor_id),
            doctor_name=doctor_name,
            appointment_day=day_code,
            appointment_date=appt_date,
            appointment_time=time_str,
            notes=notes,
        )

        return JsonResponse({
            'ok': True,
            'booking_id': appt.pk,
            'doctor': doctor_name,
            'date': appt_date.strftime('%d/%m/%Y'),
            'day': DAY_AR.get(day_code, day_code),
            'time': time_str,
            'department': department,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
