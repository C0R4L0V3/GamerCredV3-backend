from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ReportSerializer
from .models import ReportSchema


# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = ReportSchema.objects.all().order_by('id')
    serializer_class = ReportSerializer


def get_reports_by_player(request):
    player_reported = request.GET.get('player_reported')
    if not player_reported:
        return JsonResponse({'error': 'Player Id required'}, status=400)
    
    reports = ReportSchema.objects.filter(player_reported=player_reported)
    if not reports.exists():
        return JsonResponse({'nessage': 'No Reports found for the specifed player'}, status=400)
    
    reports_data = list(reports.values())
    return JsonResponse({'reports': reports_data}, status=200)