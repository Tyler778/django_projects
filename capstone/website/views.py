from django.urls import reverse, reverse_lazy
from urllib import request
from django.shortcuts import render
from sklearn import linear_model
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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
from sklearn.preprocessing import StandardScaler
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

    def pca_f(self, df):
        df_heart_disease = df
        #print(df_heart_disease)
        features = ['Age',
                    #'Sex',
                    'ChestPainType',
                    #'RestingBP',
                    'Cholesterol',
                    'FastingBS',
                    'RestingECG',
                    'MaxHR',
                    'ExerciseAngina',
                    'Oldpeak',
                    'ST_Slope']
        x = df_heart_disease.loc[:, features].values
        y = df_heart_disease.loc[:,['HeartDisease']].values
        x = StandardScaler().fit_transform(x)

        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(x)
        principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])  
        finalDf = pd.concat([principalDf, df[['HeartDisease']]], axis = 1)   
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.set_title('2 Component PCA')
        targets = [0, 1]
        colors = ['b', 'r']
        for target, color in zip(targets,colors):
            indiciesToKeep = finalDf['HeartDisease'] == target
            ax.scatter(finalDf.loc[indiciesToKeep, 'principal component 1']
                , finalDf.loc[indiciesToKeep, 'principal component 2']
                , c = color
                , s = 50)
        ax.legend([ 'No Heart Disease', 'Heart Disease'])
        ax.grid

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

    def chest_age_heart(self, df):
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

    def BP_heart(self, df):
        df_heart_disease = df[df['HeartDisease'] > 0]
        df_no_heart_disease = df[df['HeartDisease'] < 1]

        ax = df_heart_disease.plot(kind='scatter', x='Age', y='RestingBP',color='red',label='Heart Disease')
        df_no_heart_disease.plot(kind='scatter', x='Age', y='RestingBP',color='blue', ax=ax, label='No Heart Disease')
        plt.title('Blood Pressure By Age')
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode
        return b64
    
    def pie_chest_heart(self, df):
        df.drop(df[df['HeartDisease'] == 0].index, inplace=True)
        plt.figure()
        df.groupby(['ChestPainType']).sum().plot(kind='pie', y='HeartDisease', autopct='%1.0f%%')
        plt.legend(['TA','ATA', 'NAP', 'ASY'])
        plt.title('Chest Pain Type in Patients With Heart Disease')
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode
        return b64

    def pie_chest_noheart(self, df):
        df_specific = self.obtain_df()
        df_specific.drop(df[df['HeartDisease'] == 1].index, inplace=True)
        cond = df_specific['HeartDisease'] == 0
        df_specific.loc[cond, 'HeartDisease'] = 1

        plt.figure()
        df_specific.groupby(['ChestPainType']).sum().plot(kind='pie', y='HeartDisease', autopct='%1.0f%%')
        plt.legend(['TA','ATA', 'NAP', 'ASY'])
        plt.title('Chest Pain Type in Patients Without Heart Disease')
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode
        return b64

    def obtain_linear(self):
        main = self.obtain_df()
        reg_line = linReg.fit(main[['Age','Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']],main['HeartDisease'])
        return reg_line


    def get_context_data(self, **kwargs):
        df = self.obtain_df()
        context = {}

        context['chart1'] = self.chol_heart(self.obtain_df())
        context['chart2'] = self.age_heartdisease_chol(self.obtain_df())
        context['chart3'] = self.BP_heart(self.obtain_df())
        context['chart4'] = self.pie_chest_heart(self.obtain_df())
        context['chart5'] = self.pie_chest_noheart(self.obtain_df())
        context['chart6'] = self.pca_f(self.obtain_df())
        context['linear'] = self.obtain_linear().coef_
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