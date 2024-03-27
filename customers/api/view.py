from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend
from customers.models import Customer
from customers.api.serializers import CustomerSerializer
from customers.api.permissions import IsOwnerOrAdmin
from rest_framework import status


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'surName', 'customer_number', 'phone_number', 'address', 'user__username'] 
    ordering_fields = ['name', 'surName', 'phone_number', 'created_at', 'updated_at']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        user = self.request.user
        # if user.is_superuser:
        #     return queryset

        queryset = queryset.filter(user__supervisor=user)
        if not queryset:
            queryset = queryset.filter(user=user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
