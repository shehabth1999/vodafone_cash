from rest_framework import serializers
from institution.models import Institution

class SInstitution(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'