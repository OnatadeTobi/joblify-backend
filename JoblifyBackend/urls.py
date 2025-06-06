"""
URL configuration for JoblifyBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "Joblify Admin"  # Change the header
admin.site.site_title = "Joblify Admin Portal"  # Change the title
admin.site.index_title = "Welcome to Joblify Admin Portal"  # Change the index title

def api_root(request):
    return JsonResponse({"message": "Joblify API is live."})


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/auth/', include('userauth.urls')),
    path('api/jobs/', include('joblinks.urls')),
    path('api/resumes/', include('resumes.urls')),
    path('api/auth/', include('social_accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
