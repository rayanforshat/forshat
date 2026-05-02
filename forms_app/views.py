from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import TreatmentRequestForm
from .utils import send_to_receiver


def initiative(request):
    if request.method == 'POST':
        form = TreatmentRequestForm(request.POST)
        if form.is_valid():
            treatment = form.save()
            # Try to forward to receiving project (non-blocking)
            send_to_receiver(treatment)
            return redirect('forms_app:success')
        # Form has errors — fall through to render with errors
    else:
        form = TreatmentRequestForm()

    return render(request, 'forms_app/initiative.html', {'form': form})


def success(request):
    return render(request, 'forms_app/success.html')
