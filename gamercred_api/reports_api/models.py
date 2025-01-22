from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    report_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports")
    timestamp = models.DateTimeField(auto_now_add=True)
    body_text = models.TextField()

    def __str__(self):
        return f'{self.report_owner}, {self.timestamp}, {self.body_text}'