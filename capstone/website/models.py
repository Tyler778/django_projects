from django.db import models
import pandas as pd
from sklearn import linear_model
linReg = linear_model.LinearRegression()

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




import uuid
class PatientPrediction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular prediction')
    #main_df = pd.read_csv('cleanHeart.csv')
    #regu = linReg.fit(main_df[['Age','Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']],main_df['HeartDisease'])

    #tester = regu.predict([[65,0,3,140,306,1,0,87,1,1.5,0]])
    
    def predict(self, Patient):
        prediction_score = self.regu.predict([[Patient.age, Patient.sex, Patient, ]])
        return prediction_score
