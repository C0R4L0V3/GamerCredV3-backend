from rest_framework import serializers
from .models import ReportSchema

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSchema
        fields = '__all__'