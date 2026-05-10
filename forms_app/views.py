from django.shortcuts import render, redirect

from .forms import TreatmentRequestForm


def initiative(request):
    if request.method == 'POST':
        form = TreatmentRequestForm(request.POST)
        if form.is_valid():
            form.save()          # signal fires automatically in background
            return redirect('forms_app:success')
        # Form has errors — fall through to render with errors
    else:
        form = TreatmentRequestForm()

    return render(request, 'forms_app/initiative.html', {'form': form})


def success(request):
    return render(request, 'forms_app/success.html')
