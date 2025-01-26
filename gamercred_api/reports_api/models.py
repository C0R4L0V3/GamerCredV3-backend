from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ReportSchema(models.Model):
    report_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports")
    player_reported =models.CharField(max_length=30)
    game_id = models.CharField(max_length=100)
    #player experiences
    harrassment = models.BooleanField(default=False)
    bullying = models.BooleanField(default=False)
    racism = models.BooleanField(default=False)
    sexual_harrasment = models.BooleanField(default=False)
    homo_transphobia = models.BooleanField(default=False)
    griefing = models.BooleanField(default=False)
    teamwork = models.BooleanField(default=False)
    friendly_helpful = models.BooleanField(default=False)
    mentorship = models.BooleanField(default=False)
    sportsmanship = models.BooleanField(default=False)
    inclusive = models.BooleanField(default=False)
    #media urls
    images_url = models.CharField(max_length=200, blank=True, null=True)
    video_url = models.CharField(max_length=200, blank=True, null=True)
    
    body_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.report_owner}, {self.game_id}, {self.timestamp}, {self.body_text}'