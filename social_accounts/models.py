from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GitHubUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_id = models.CharField(max_length=255, unique=True)
    github_login = models.CharField(max_length=255)
    github_access_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.github_login}"
