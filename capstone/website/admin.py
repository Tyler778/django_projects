from django.contrib import admin
from .models import Patient
# Register your models here.
#admin.site.register(Patient)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('age', 'sex', 'chest', 'restingBP', 'cholesterol', 'fastingBS', 'ecg', 'maxHR', 'exerciseAngina', 'oldPeak', 'stSlope')
    list_filter = ('age', 'sex')

admin.site.register(Patient, PatientAdmin)