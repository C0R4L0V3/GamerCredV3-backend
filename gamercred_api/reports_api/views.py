from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ReportSerializer
from .models import ReportSchema

# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = ReportSchema.objects.all().order_by('id')
    serializer_class = ReportSerializer
