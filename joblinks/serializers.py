from rest_framework import serializers
from .models import JobLink

class JobLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLink
        fields = ['id', 'title', 'company', 'platform', 'created_at']
        read_only_fields = ['id', 'created_at']
