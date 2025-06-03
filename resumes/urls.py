from django.urls import path
from .views import ResumeUploadView, ResumeJsonDetailView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('resume/', ResumeJsonDetailView.as_view(), name='resume-detail'),
]
