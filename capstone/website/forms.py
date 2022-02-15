from django.forms import ModelForm
from website.models import Patient

class CheckPatient(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'