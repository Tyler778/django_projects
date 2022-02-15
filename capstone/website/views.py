from django.urls import reverse
from urllib import request
from django.shortcuts import render
from .models import Patient
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.



def index(request):
    """View function for home page of site."""

    # Generate Count of Patients entered
    num_patients = Patient.objects.all().count()

    context = {
        'num_patients': num_patients,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class PatientCreate(CreateView):
    model = Patient
    fields = '__all__'

    def get_success_url(self):
        return reverse('index')
