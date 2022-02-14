from django.db import models

# Create your models here.
class Patient(models.Model):
    """Model Representing the Patient."""
    age = models.IntegerField(help_text='Enter age of patient')
    sex_fields = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(
        max_length=1,
        choices=sex_fields,
        blank=True,
        help_text='Sex of patient',
    )
    chest_fields = (
        ('TA', 'Typical Angina'),
        ('ATA', 'Atypical Angina'),
        ('NAP', ' Non-Anginal Pain'),
        ('ASY', 'Asymptomatic'),
    )
    chest = models.CharField(
        max_length=3,
        choices=chest_fields,
        blank=True,
        help_text='Chest Pain Type of patient',
    )
    restingBP = models.IntegerField(help_text='Enter Resting BP of patient')
    cholesterol = models.IntegerField(help_text='Enter Cholesterol of patient')
    fastingBS = models.IntegerField(help_text='Enter fasting blood sugar of patient')
    ecg_fields = (
        ('Normal', 'Normal'),
        ('ST', 'having ST-T wave abnormality'),
        ('LVH', 'showing probable or definite left ventricular hypertrophy by Estes criteria'),
    )
    ecg = models.CharField(
        max_length = 8,
        choices = ecg_fields,
        blank=True,
        help_text='Resting ECG analysis of patient',
    )
    maxHR = models.IntegerField(help_text='Enter the max heart rate of the patient')
    exerciseAngina_fields = (
        ('Y', "yes"),
        ('N', 'no')
    )
    exerciseAngina = models.CharField(
        max_length = 1,
        choices = exerciseAngina_fields,
        help_text = 'Does the patient experience exercise induced angina?'
    )
    oldPeak = models.FloatField(max_length = 4, help_text = 'Enter oldpeak measured in depression')
    st_slope_fields = (
        ('Up', 'Upwards'),
        ('Flat', 'Flat'),
        ('Down', 'Downwards')
    )
    stSlope = models.CharField(
        max_length = 10,
        choices = st_slope_fields,
        help_text = 'Enter the slope of the peak exercise ST segment direction for the patient',
    )





    def __str__(self):
        """String for representing the Model object."""
        return self.name
