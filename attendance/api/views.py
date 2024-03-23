# ------------ API AND  APIVIEW AND VIEWSETS-----------#
# API UTILS
from rest_framework import status
from rest_framework.response import Response

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
from institution.models import Institution
from institution.api.serializers import SInstitution
from core.utils.response import MainResponse
# Swagger API
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator


class InstitutionMVS(viewsets.ModelViewSet,MainResponse):
    queryset = Institution.objects.all()
    serializer_class = SInstitution
    filter_backends     = [OrderingFilter,DjangoFilterBackend]
    filterset_fields    = '__all__'
    ordering_fields     = '__all__'
    main_operation_description = "description "
    main_operation_summary="sdsd"
    main_tags=["Institution"]

    @method_decorator(name='list', decorator=swagger_auto_schema(operation_description=main_operation_description,operation_summary=main_operation_summary,tags=main_tags))
    def list(self, request, *args, **kwargs):
        return self.returnReponse(action=self.RETREIVE,body=super(InstitutionMVS, self).list(request, *args, **kwargs))

    @method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description=main_operation_description,operation_summary=main_operation_summary,tags=main_tags))
    def retrieve(self, request, *args, **kwargs):
        return self.returnReponse(action=self.RETREIVE,body=super(InstitutionMVS, self).retrieve(request, *args, **kwargs))

    @method_decorator(name='update', decorator=swagger_auto_schema(operation_description=main_operation_description,operation_summary=main_operation_summary,tags=main_tags))
    def update(self, request, *args, **kwargs):
        return self.returnReponse(action=self.PUT,body=super(InstitutionMVS, self).update(request, *args, **kwargs))

    @method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_description=main_operation_description,operation_summary=main_operation_summary,tags=main_tags))
    def partial_update(self, request, *args, **kwargs):
        return self.returnReponse(action=self.PUT,body=super(InstitutionMVS, self).partial_update(request, *args, **kwargs))

    @method_decorator(name='create', decorator=swagger_auto_schema(operation_description=main_operation_description,operation_summary=main_operation_summary,tags=main_tags))
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return self.returnReponse(action=self.POST,body=super(InstitutionMVS, self).create(request, *args, **kwargs))

    @method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description=main_operation_description,operation_summary=main_operation_summary,tags=main_tags))
    def destroy(self, request, *args, **kwargs):
        return self.returnReponse(action=self.DELETE,body=super(InstitutionMVS, self).destroy(request, *args, **kwargs))
    
