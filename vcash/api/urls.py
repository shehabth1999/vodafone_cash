from vcash.api import views as api 
from rest_framework import routers
from django.urls import path,include

router = routers.DefaultRouter()
router.register('transactions',api.TransactionsCashMVS,basename="transactions-cash-mvs")
router.register('sim'         ,api.SimMVS)
router.register('sim-log'     ,api.SimLogMVS)
router.register('device'      ,api.DeviceMVS)
urlpatterns = [
    path('', include(router.urls)),
    ]

