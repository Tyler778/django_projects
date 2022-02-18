from django.urls import reverse, reverse_lazy
from urllib import request
from django.shortcuts import render
from sklearn import linear_model
from .models import AccuracyModel, Patient, Visualization
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import urllib, base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, base64
from django.db.models.functions import TruncDay
from matplotlib.ticker import LinearLocator
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

class DataViewOne(LoginRequiredMixin, generic.ListView):
    model = Visualization
    

    def obtain_df(self):
        df = pd.read_csv('https://bscs-capstone-tyler.s3.us-east-2.amazonaws.com/cleanHeart.csv')
        return df

    def chol_heart(self, df):
        df_heart_disease = df[df['HeartDisease'] > 0]
        df_no_heart_disease = df[df['HeartDisease'] < 1]

        ax = df_heart_disease.plot(kind='scatter', x='Age', y='MaxHR',color='red',label='Heart Disease')
        df_no_heart_disease.plot(kind='scatter', x='Age', y='MaxHR',color='blue', ax=ax, label='No Heart Disease')
        plt.title('Max Heart Rate by Age')
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode
        return b64
    
    def age_heartdisease_chol(self, df):
        df_heart_disease = df[df['HeartDisease'] > 0]
        df_heart_disease = df_heart_disease[df_heart_disease['Cholesterol'] > 0]
        df_no_heart_disease = df[df['HeartDisease'] < 1]
        df_no_heart_disease = df_no_heart_disease[df_no_heart_disease['Cholesterol'] > 0]


        ax = df_heart_disease.plot(kind='scatter', x='Age', y='Cholesterol',color='red',label='Heart Disease')
        df_no_heart_disease.plot(kind='scatter', x='Age', y='Cholesterol',color='blue', ax=ax, label='No Heart Disease')
        plt.title('Cholesterol in Different Ages')
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode
        return b64
    



    def get_context_data(self, **kwargs):



        df = self.obtain_df()
        context = {}

        context['chart1'] = self.chol_heart(df)

        context['chart2'] = self.age_heartdisease_chol(df)
        return context

linReg = linear_model.LinearRegression()
class AccuracyTestView(LoginRequiredMixin, generic.ListView):
    model = AccuracyModel

    def obtain_df(self):
        df = pd.read_csv('https://bscs-capstone-tyler.s3.us-east-2.amazonaws.com/cleanHeart.csv')
        return df

    def perform_prediction_disease(self):
        main = self.obtain_df()
        regu = linReg.fit(main[['Age','Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']],main['HeartDisease'])
        heart_disease = []
        for i in range(len(AccuracyModel.heart_disease_testers)):
            test = regu.predict([[
                AccuracyModel.heart_disease_testers[i][0],
                AccuracyModel.heart_disease_testers[i][1],
                AccuracyModel.heart_disease_testers[i][2],
                AccuracyModel.heart_disease_testers[i][3], 
                AccuracyModel.heart_disease_testers[i][4], 
                AccuracyModel.heart_disease_testers[i][5], 
                AccuracyModel.heart_disease_testers[i][6], 
                AccuracyModel.heart_disease_testers[i][7], 
                AccuracyModel.heart_disease_testers[i][8],
                AccuracyModel.heart_disease_testers[i][9],
                AccuracyModel.heart_disease_testers[i][10]]])
            heart_disease.append(self.determine_severity(test))
        print(heart_disease)
        
        return heart_disease

    def perform_prediction_non_disease(self):
        main = self.obtain_df()
        regu = linReg.fit(main[['Age','Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']],main['HeartDisease'])
        heart_non_disease = []
        for i in range(len(AccuracyModel.non_heart_disease_testers)):
            test = regu.predict([[
                AccuracyModel.non_heart_disease_testers[i][0],
                AccuracyModel.non_heart_disease_testers[i][1],
                AccuracyModel.non_heart_disease_testers[i][2],
                AccuracyModel.non_heart_disease_testers[i][3], 
                AccuracyModel.non_heart_disease_testers[i][4], 
                AccuracyModel.non_heart_disease_testers[i][5], 
                AccuracyModel.non_heart_disease_testers[i][6], 
                AccuracyModel.non_heart_disease_testers[i][7], 
                AccuracyModel.non_heart_disease_testers[i][8],
                AccuracyModel.non_heart_disease_testers[i][9],
                AccuracyModel.non_heart_disease_testers[i][10]]])
            heart_non_disease.append(self.determine_severity(test))
        print(heart_non_disease)
        
        return heart_non_disease

    def determine_severity(self, val):
        if val < .20:
            return 'blue'
        elif val < .4:
            return 'yellow'
        elif val < .55:
            return 'orange'
        elif val < .7:
            return 'red'
        elif val < 2.0:
            return 'Absolute'

    def get_context_data(self, **kwargs):
        df = self.obtain_df()
        heart_dictionary = {}
        non_heart_dictionary = {}
        context = {
            'heartdict': heart_dictionary,
            'nonheartdict': non_heart_dictionary
        }
        severity_list = self.perform_prediction_disease()
        severity_list_2 = self.perform_prediction_non_disease()
        for i in range(len(severity_list_2)):
            non_heart_dictionary[i] = severity_list_2[i]
        for i in range(len(severity_list)):
            heart_dictionary[i] = severity_list[i]
            
        return context