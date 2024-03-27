from django.urls import path, include

urlpatterns = [
    path('api/', include('customers.api.urls'), name='customers.api'),
]
