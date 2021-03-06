"""capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from website.views import PatientCreate, PatientListView, PatientDetailView, PatientDelete, DataViewOne, AccuracyTestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('website/', include('website.urls')),
    path('', RedirectView.as_view(url='website/', permanent=True)),
    path('patient/create/', PatientCreate.as_view(), name='patient-create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('patients/', PatientListView.as_view(), name='patients'),
    path('patient/<int:pk>', PatientDetailView.as_view(), name='patient-detail'),
    path('patient/<int:pk>/delete/', PatientDelete.as_view(), name='patient-delete'),
    path('visualization', DataViewOne.as_view(), name='visual'),
    path('accuracy', AccuracyTestView.as_view(), name='accuracy'),
]







# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
