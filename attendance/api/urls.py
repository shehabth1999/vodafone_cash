from django.urls import include,path
from rest_framework import routers
from institution.api import views as api
from ..apps import __package__ as appName


institution = routers.DefaultRouter()
institution.register(appName,api.InstitutionMVS)
urlpatterns = [
    path('',include(institution.urls)),
    
]
