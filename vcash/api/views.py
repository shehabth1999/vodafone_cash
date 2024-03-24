# ------------ API AND  APIVIEW AND VIEWSETS-----------#
import datetime
from typing_extensions import dataclass_transform
from django.contrib.auth import authenticate
# API UTILS
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse

from rest_framework.decorators import action
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView  # ListAPIView
from rest_framework import viewsets  			 # VIEWSETS
from rest_framework.views import APIView  		 # APIVIEW
# ------------ SERIALIZERS AND MODEL -----------#
from vcash.models import SimLog,Sim,Device,TransactionsCash
from vcash.api.serializers import (
    SSim,SSimLog,SDevice,STransactionsCash,SSimCollection,SDeviceCollection,
    STransactionsCashCollection,SSimCollectionRetrieve,Gard)
# Swagger API
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from vcash.api.pagination import LargeResultsSetPagination

class SimMVS(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination
    queryset            = Sim.objects.all()
    serializer_class    = SSim
    filter_backends     = [OrderingFilter,DjangoFilterBackend]
    filterset_fields    = '__all__'
    ordering_fields     = [
                    'phone',    
                    'number',   
                    'note',     
                    'value',    
                    'isused',   
                    'device', 
                    'device__name',    
                    'user',     
                    'datetime', 
                    'slot',
                    ]
    lookup_field        = 'phone'

    @action(methods=["GET",],detail=False,url_path="phone_list",url_name="phone_list")
    def getSimsListAsPhone(self,request):
        return Response([i["phone"] for i in self.queryset.values("phone")])


    @action(methods=["GET",],detail=False,url_path="dialy_gard",url_name="dialy_gard")
    def dialyGardSim(self,request):
        currentDate = str(datetime.datetime.now().date())
        date = request.query_params.get("date",currentDate)

        currentSims = TransactionsCash.objects.filter(date=date)\
                    .order_by('sim_id')\
                    .distinct('sim')\
                    .values_list('sim',flat=True)

        sims = Sim.objects.filter(id__in=currentSims).order_by('isused','device__name','number')
        return Response({"results":Gard(sims,many=True,context = {"date":date}).data})

    @action(methods=["POST",],detail=False,url_path="insert_remove_sim",url_name="insert_remove_sim")
    def insertAndRemoveSim(self,request):
        """
        # insert and remove sim
        -----------------------
        1 - get number and get device number and slot and datetime (Inputs)
        2- check if this number recorded before
        3- check if this device recorded before
        4- check if this number is the same of last number of log sim
            1- get last recorded log sim
            2- make if condition
        5- update remove record date ,time and datetime of last number
        6 - record insert record date,time and datetime of new number
        """
        number = request.query_params.get('number','')
        iemi = request.query_params.get('imei','')
        slot = request.query_params.get('slot',-1)
        date  = datetime.datetime.now().date()
        time  = datetime.datetime.now().time()
        dateTime  = datetime.datetime.now()

        try:
            
            cSim = Sim.objects.get(phone = number)
            try:   device = Device.objects.get(imei = iemi)
            except Device.DoesNotExist: device  = None
            
            oSim = SimLog.objects.filter(sim__phone = number,isLast = False, isFirst=False).last()

            if oSim == None:  # if there is no log
                
                cSim.isused = True
                cSim.device = device
                cSim.slot   = slot
                cSim.save()

                # insert new simLog
                nSim = SimLog()
                nSim.sim = cSim
                nSim.value = cSim.value
                nSim.timeinsert = time
                nSim.datetimeinsert = dateTime
                nSim.dateinsert = date
                nSim.save()
                return Response({"result":'تم تغيير الشريحه بنجاح','status':True})

            if oSim.sim.phone == cSim.phone:
                # update remove
                oSim.timeremove = time
                oSim.datetimeremove = dateTime
                oSim.dateremove = date
                oSim.save()

                # الشريحه القديمه
                oSi = oSim.sim
                oSi.isused = False
                oSi.device = None
                oSi.slot = -1
                oSi.save()

                # الشريحه الحاليه
                cSim.isused = True
                cSim.device = device
                cSim.slot = slot
                cSim.save()

                # insert new sim Log
                nSim = SimLog()
                nSim.sim = cSim
                nSim.value = cSim.value
                nSim.timeinsert = time
                nSim.datetimeinsert = dateTime
                nSim.dateinsert = date
                nSim.save()
                return Response({"result":'تم تغيير الشريحه بنجاح','status':True})
            return Response({"result":'الشريحه الحالية لم تتغير','status':False})
        except Sim.DoesNotExist:
            return Response({"result":'لم يتم تسجيل هذه الشريحه','status':False})

    @action(methods=["POST",],detail=False,url_path="remove_sim",url_name="remove_sim")
    def removeRemoveSim(self,request):
        number = request.query_params.get('number','')
        try:
            date  = datetime.datetime.now().date()
            time  = datetime.datetime.now().time()
            dateTime  = datetime.datetime.now()

            cSim = Sim.objects.get(phone = number)
            oSim = SimLog.objects.filter(sim__phone = number ,isLast = False, isFirst=False).last()


            if oSim == None:  # if there is no log
                cSim.isused = False
                cSim.device = None
                cSim.slot   = -1
                cSim.save()


            if oSim.sim.phone == cSim.phone:
                # update remove
                oSim.timeremove = time
                oSim.datetimeremove = dateTime
                oSim.dateremove = date
                oSim.save()

                # الشريحه الحاليه
                cSim.isused = False
                cSim.device = None
                cSim.slot   = -1
                cSim.save()

            return Response({"result":'تم نزع الشريحه بنجاح','status':True})
        except Sim.DoesNotExist:
            return Response({"result":'لم يتم تسجيل هذه الشريحه','status':False})
    
    @action(methods=["PUT",],detail=False,url_path="update-coast",url_name="update-coast")
    def updateCoast(self,request):
        """update coast"""
        user = request.user
        number = request.query_params.get('number','')
        coast  = request.query_params.get('coast','0')
        currentDatetime = datetime.datetime.now()
        currentDate     = currentDatetime.date()
        currentTime     = currentDatetime.time()
        try:
            # Update SIM coast and Date
            sim           = Sim.objects.get(phone = number)
            sim.value     = coast
            sim.datetime  = currentDatetime
            sim.save()

            # Update First coast
            simLogFirst = SimLog.objects.filter(dateinsert = currentDate,isFirst = True,sim = sim)
            if len(simLogFirst) == 0:
                SimLog(
                    datetimeinsert=currentDatetime ,
                    dateinsert = currentDate,
                    timeinsert = currentTime,
                    value = coast,
                    sim =sim,
                    isFirst = True
                    ).save()
            
            # Update Last coast
            simLogLast = SimLog.objects.filter(dateinsert = currentDate,isLast = True,sim = sim)
            if len(simLogLast) == 0:
                SimLog(
                    datetimeinsert=currentDatetime ,
                    dateinsert = currentDate,
                    timeinsert = currentTime,
                    value = coast,
                    sim =sim,
                    isLast = True
                    ).save()
            else:
                simLogLast.update(value = coast)

            # record transaction history
            TransactionsCash(
                sim = sim,     
                user = user,     
                customer = number,   
                value = coast,     
                rest = 0,     
                note  = "إستعلام رصيد",    
                date = currentDate,
                time = currentTime,
            ).save()

        except Sim.DoesNotExist:
            return Response({"result":'لم يتم تسجيل هذه الشريحه','status':False})
        return Response({"result":'تم تحديث الرصيد','status':True})

    def partial_update(self, request, *args, **kwargs):
        super(SimMVS, self).partial_update(request, *args, **kwargs)
        return Response({"message": "تم تعديل الشريحة بنجاح","status":  True})

    def update(self, request, *args, **kwargs):
        request.data["datetime"] = str(datetime.datetime.now())
        super(SimMVS, self).update(request, *args, **kwargs)
        return Response({"message": "تم تعديل الشريحة بنجاح","status":  True})
        
    def list(self, request, *args, **kwargs):
        self.serializer_class = SSimCollection
        return super(SimMVS, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup =  self.kwargs[lookup_url_kwarg]

            sim = Sim.objects.get(phone  =  lookup)
            sim.isused = True
            sim.save()
            return Response(SSimCollectionRetrieve(sim,many=False).data)
        except Sim.DoesNotExist as e:
            return Response({"message": "لا يوجد شريحه","status":  True})
        
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        super(SimMVS, self).create(request, *args, **kwargs)
        return Response({"message": "تم إضافه الشريحة بنجاح","status":  True})
    
    def destroy(self, request, *args, **kwargs):
        super(SimMVS, self).destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف الشريحة بنجاح","status":  True})

class SimLogMVS(viewsets.ModelViewSet):
    queryset            = SimLog.objects.all()
    serializer_class    = SSimLog
    filter_backends     = [OrderingFilter,DjangoFilterBackend]
    filterset_fields    = '__all__'
    ordering_fields     = '__all__'
    def update(self, request, *args, **kwargs):
        super(SimLogMVS, self).update(request, *args, **kwargs)
        return Response({"message": "تم تعديل الشريحة بنجاح","status":  True})
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        super(SimLogMVS, self).create(request, *args, **kwargs)
        return Response({"message": "تم إضافه الشريحة بنجاح","status":  True})
    def destroy(self, request, *args, **kwargs):
        super(SimLogMVS, self).destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف الشريحة بنجاح","status":  True})

class DeviceMVS(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = SDevice
    filter_backends     = [OrderingFilter,DjangoFilterBackend]
    filterset_fields    = '__all__'
    ordering_fields     = '__all__'
    #lookup_field        = 'imei'

    def list(self, request, *args, **kwargs):
        self.serializer_class = SDeviceCollection
        return super(DeviceMVS, self).list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            data = Device.objects.get(imei=kwargs[self.lookup_field])
            return Response(SDeviceCollection(data,many=False).data)
        except Device.DoesNotExist:
            data = Device()
            data.name = request.query_params.get('name','')
            data.deviceid = request.query_params.get('deviceid','')
            data.imei = request.query_params.get('imei','')
            data.baddress = request.query_params.get('baddress','')
            data.user = request.user
            data.save()
            return Response(SDeviceCollection(data,many=False).data)
    
    def update(self, request, *args, **kwargs):
        super(DeviceMVS, self).update(request, *args, **kwargs)
        return Response({"message": "تم تعديل الجهاز بنجاح","status":  True})
    
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        super(DeviceMVS, self).create(request, *args, **kwargs)
        return Response({"message": "تم إضافه الجهاز بنجاح","status":  True})

    
    def destroy(self, request, *args, **kwargs):
        super(DeviceMVS, self).destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف الجهاز بنجاح","status":  True})

class DateFilter(filters.FilterSet):
    month = filters.NumberFilter(field_name='date__month', lookup_expr='exact')
    year = filters.NumberFilter(field_name='date__year', lookup_expr='exact')

    class Meta:
        model = TransactionsCash
        fields = ["device","sim_id","sim__isused","sim__device","sim__phone","sim__number","user","user__username","customer","value","isSend","date",'month','year']

class MyCustomOrdering(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if "month" in ordering:
            if len(ordering) > 1:
                pass

        else: return queryset.order_by(*ordering)
        return queryset

class TransactionsCashMVS(viewsets.ModelViewSet):
    queryset = TransactionsCash.objects.all()
    serializer_class    = STransactionsCash
    filter_backends     = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filter_class        = DateFilter
    search_fields       = ["note","customer","operationno"]
    ordering_fields     = ['timestamp','datetime','time','value', 'rest','month']
    
    @action(methods=['GET',],detail=False,url_name="phone-list",url_path="phone-list")
    def getPhoneList(self,request):
        customers = [i['customer'] for i in  TransactionsCash.objects.all().values('customer').order_by('customer').distinct('customer')]
        phones = [i["phone"] for i in Sim.objects.all().values("phone")]
        return Response(customers+phones)
        
    def list(self, request, *args, **kwargs):
        self.serializer_class = STransactionsCashCollection
        return super(TransactionsCashMVS, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = STransactionsCashCollection
        return super(TransactionsCashMVS, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super(TransactionsCashMVS, self).update(request, *args, **kwargs)
        return Response({"message": "تم تعديل التحويل بنجاح","status":  True})

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        
        kwargs = dict(request.data)
        
        
        if 'time' in kwargs: del kwargs['time']
        if 'timestamp' in kwargs: del kwargs['timestamp'] 
        if 'isServer' in kwargs: del kwargs['isServer']

        obj = TransactionsCash.objects.filter(**kwargs)
        
        if len(obj) == 0:
            super(TransactionsCashMVS, self).create(request, *args, **kwargs)
            return Response({"message": "تم إضافه التحويل بنجاح","status":  True})

        else:

            times  = [( datetime.datetime.now() - o.datetime ).total_seconds() > 30 for o in obj ] 
            state =  False in times 
            if state:
                return Response({"message": "التحويل متكرر","status":  False})
            else:
                super(TransactionsCashMVS, self).create(request, *args, **kwargs)
                return Response({"message": "تم إضافه التحويل بنجاح","status":  True})
                

        
    def destroy(self, request, *args, **kwargs):
        super(TransactionsCashMVS, self).destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف التحويل بنجاح","status":  True})