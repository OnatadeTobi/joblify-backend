from django.urls import path
from .views import GoogleSignInView, GitHubSignInView

urlpatterns = [
    path('google/', GoogleSignInView.as_view(), name='google-sign-in'),
    path('github/', GitHubSignInView.as_view(), name='github-sign-in'),
]