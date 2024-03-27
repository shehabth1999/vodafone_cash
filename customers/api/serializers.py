from rest_framework import serializers
from customers.models import Customer
from django.db.models import Q
import re

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'surName', 'customer_number', 'phone_number', 'address', 'rest', 'user', 'updated_at', 'created_at']
        extra_kwargs = {
            'customer_number': {'required': False},
            'rest': {'required': False},
        }

    def create(self, validated_data):
        if not validated_data['user'] :
            validated_data['user'] = self.context['request'].user
            
        validated_data['rest'] = 0
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        surName = data.get('surName')
        phone_number = data.get('phone_number')

        errors = []

        if name == surName:
            errors.append({'name':"Name and surName cannot be the same"})
            errors.append({'surName':"Name and surName cannot be the same"})
        
        # user_customers = Customer.objects.filter(user=user)
        # if user <= user_customers.count():
        #     errors.append({"error":"This Account has Reached max number of Customers"}) 

        if self.context['request'].method in ['PUT', 'PATCH']:
            user_customers = user_customers.exclude(Q(user=user,name=name,surName=surName,phone_number=phone_number))

        user_and_name = user_customers.filter(user=user, name=name).exists()
        user_and_surName = user_customers.filter(user=user, surName=surName).exists()
        user_and_phone_number = user_customers.filter(user=user, phone_number=phone_number).exists()

        if user_and_name:
            errors.append({"name":"This name alredy exists"}) 
        if user_and_surName:
            errors.append({"surName":"This surName alredy exists"}) 
        if user_and_phone_number:
            errors.append({"phone_number":"This phone_number alredy exists"}) 

        if not re.match(r'^\+?\d{10,15}$', phone_number):
            errors.append({"phone_number":"Invalid phone number format. It should be 10-15 digits, optionally starting with '+'."})  

        if len(name) < 3:
            errors.append({"name":"Name must be at least 3 characters long."})   
              
        if errors:
            raise serializers.ValidationError(errors)
        
        return data