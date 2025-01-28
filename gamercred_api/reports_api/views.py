from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ReportSerializer
from .models import ReportSchema
from .forms import ReportForm
import logging

logger = logging.getLogger(__name__)

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

#create a report
def create_report(req):
    if req.method == 'POST':
        form = ReportForm(req.POST, req.FILES)
        if form.is_valid():
            #save teh report
            report = form.save(commit=False)
            #setting the report_owner to the currently authenticated user
            report.report_owner = req.user
            report.save()

            #access teh files URLS and save them to the reports_api DB
            if report.image:
                logger.info(f"Image uploaded: {report.images.url}")
                report.image_url = report.image.url
            if report.video:
                report.video_url = report.video.url

            print(report.video_url)
            print(report.image_url)
            
            report.save()



            # print(report_instance.image.url)

            # I want it to redirect back to the list page
            return redirect('get_reports_player')
        
    else:
        form = ReportForm()
    
    return render(req, 'create_report.html', {'form': form})