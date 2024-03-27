from django.urls import path,include

urlpatterns = [
    path('api/',include('vcash.api.urls'), name='vcash.api')
]