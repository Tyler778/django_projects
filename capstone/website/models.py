from django.db import models
from django.urls import reverse
import pandas as pd
from sklearn import linear_model
from django.contrib.staticfiles import *
import csv
linReg = linear_model.LinearRegression()

# Create your models here.
class Patient(models.Model):
    """Model Representing the Patient."""
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular patient')
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
        ('ST', 'Having ST-T wave abnormality'),
        ('LVH', 'Left Ventricular Hypertrophy'),
    )
    ecg = models.CharField(
        max_length = 8,
        choices = ecg_fields,
        blank=True,
        help_text='Resting ECG analysis of patient',
    )
    maxHR = models.IntegerField(help_text='Enter the max heart rate of the patient')
    exerciseAngina_fields = (
        ('Yes', "Yes"),
        ('No', 'No')
    )
    exerciseAngina = models.CharField(
        max_length = 3,
        choices = exerciseAngina_fields,
        help_text = 'Does the patient experience exercise induced angina?'
    )
    oldPeak = models.FloatField(max_length = 4, help_text = 'Enter oldpeak measured in depression')
    st_slope_fields = (
        ('Upwards', 'Upwards'),
        ('Flat', 'Flat'),
        ('Down', 'Down')
    )
    stSlope = models.CharField(
        max_length = 10,
        choices = st_slope_fields,
        help_text = 'Enter the slope of the peak exercise ST segment direction for the patient',
    )

    def __str__(self):
        """String for representing the Model object."""
        return str(self.age)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this patient."""
        return reverse('patient-detail', args=[str(self.id)])

    def get_absolute_url_delete(self):
        """Returns the url to access a detail record for this patient."""
        return reverse('patient-delete', args=[str(self.id)])

    def ping_me(self):
        return 'ping!'

    def perform_prediction(self):
        main = pd.read_csv('https://bscs-capstone-tyler.s3.us-east-2.amazonaws.com/cleanHeart.csv')
        regu = linReg.fit(main[['Age','Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']],main['HeartDisease'])
        tester = regu.predict([self.clean_attributes()])
        return tester[0]

    def clean_attributes(self):
        binAge = int(self.age)

        if self.sex == 'M':
            binSex = 0
        elif self.sex == 'F':
            binSex = 1
        
        if self.chest == 'TA':
            binChest = 0
        elif self.chest == 'ATA':
            binChest = 1
        elif self.chest == 'NAP':
            binChest = 2
        elif self.chest == 'ASY':
            binChest = 3

        binRestingBP = int(self.restingBP)
        binCholesterol = int(self.cholesterol)
        binFastingBS = int(self.fastingBS)

        if self.ecg == 'Normal':
            binECG = 0
        elif self.ecg == 'ST':
            binECG = 1
        elif self.ecg == 'LVH':
            binECG = 2
        if self.exerciseAngina == 'Yes':
            binExerciseAngina = 1
        elif self.exerciseAngina == 'No':
            binExerciseAngina = 0
        
        binMaxHR = int(self.maxHR)
        binOldPeak = float(self.oldPeak)

        if self.stSlope == 'Flat':
            binSTSlope = 0
        elif self.stSlope == 'Down':
            binSTSlope = -1
        elif self.stSlope == 'Upwards':
            binSTSlope = 1
        patientInfo = [binAge, binSex, binChest, binRestingBP, binCholesterol, binFastingBS, binECG, binMaxHR, binExerciseAngina, binOldPeak, binSTSlope]
        return patientInfo