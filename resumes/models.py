from django.db import models
from JoblifyBackend import settings

# Create your models here.

class ParsedResume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    raw_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}'s Resume ({self.created_at.date()})"
