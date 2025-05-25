from django.urls import path
from .views import FetchJobInfoView

urlpatterns = [
    path('fetch/', FetchJobInfoView.as_view(), name='fetch-job-info'),
]
