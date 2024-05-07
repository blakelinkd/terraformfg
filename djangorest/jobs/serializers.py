from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        extra_kwargs = {
            'url': {'required': True},
            'title': {'required': True},
            'company_name': {'required': True},
        }