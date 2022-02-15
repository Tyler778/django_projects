from django.urls import reverse, reverse_lazy
from urllib import request
from django.shortcuts import render
from .models import Patient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
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

class PatientCreate(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Patient
    fields = ('age', 'sex', 'chest', 'restingBP', 'cholesterol', 'fastingBS', 'ecg', 'maxHR', 'exerciseAngina', 'oldPeak', 'stSlope')

    def get_success_url(self):
        return reverse('patients')

class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient

class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Patient

class PatientDelete(LoginRequiredMixin, generic.DeleteView):
    model = Patient
    success_url = reverse_lazy('patients')

