from django.urls import path
from .views import FetchJobInfoView, JobLinkListCreateView, JobLinkDetailView

urlpatterns = [
    path('fetch/', FetchJobInfoView.as_view(), name='fetch-job-info'),
    #path('save/', SaveJobLinkView.as_view(), name='save-job-link'),
    #path('list/', JobLinkListView.as_view(), name='list-job-info'),
    path('jobs/', JobLinkListCreateView.as_view(), name='joblink-list-create'),
    path('jobs/<int:pk>/', JobLinkDetailView.as_view(), name='joblink-detail'),
]
