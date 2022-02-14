from django.shortcuts import render

# Create your views here.

from .models import Patient

def index(request):
    """View function for home page of site."""

    # Generate Count of Patients entered
    num_patients = Patient.objects.all().count()

    context = {
        'num_patients': num_patients,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
