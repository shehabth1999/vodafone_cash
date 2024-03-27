from customers.api import view as api
from rest_framework import routers
from django.urls import path,include

router = routers.DefaultRouter()
router.register('customers', api.CustomerView)

urlpatterns = [
    path('', include(router.urls)),
]
