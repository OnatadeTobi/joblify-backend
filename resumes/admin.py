from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ParsedResume
import json

@admin.register(ParsedResume)
class ParsedResumeAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('user_info', 'resume_title', 'skills_count', 'experience_count', 'created_at', 'view_resume')
    
    # Add filters
    list_filter = ('created_at',)
    
    # Add search functionality
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'raw_json__Name')
    
    # Add date hierarchy
    date_hierarchy = 'created_at'
    
    # Fields to show in the detail view
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'created_at')
        }),
        ('Resume Content', {
            'fields': ('formatted_json',),
            'classes': ('collapse',)
        }),
    )
    
    # Make certain fields read-only
    readonly_fields = ('created_at', 'formatted_json')
    
    # Add list per page option
    list_per_page = 20
    
    # Add ordering
    ordering = ('-created_at',)
    
    def user_info(self, obj):
        return f"{obj.user.get_full_name} ({obj.user.email})"
    user_info.short_description = "User"
    
    def resume_title(self, obj):
        try:
            data = json.loads(obj.raw_json) if isinstance(obj.raw_json, str) else obj.raw_json
            return f"{data.get('Name', 'N/A')} - {data.get('Position', 'N/A')}"
        except:
            return "Invalid JSON"
    resume_title.short_description = "Resume"
    
    def skills_count(self, obj):
        try:
            data = json.loads(obj.raw_json) if isinstance(obj.raw_json, str) else obj.raw_json
            skills = data.get('Skills', [])
            return len(skills)
        except:
            return 0
    skills_count.short_description = "Skills"
    
    def experience_count(self, obj):
        try:
            data = json.loads(obj.raw_json) if isinstance(obj.raw_json, str) else obj.raw_json
            experiences = data.get('Experience', [])
            return len(experiences)
        except:
            return 0
    experience_count.short_description = "Experience"
    
    def formatted_json(self, obj):
        try:
            data = json.loads(obj.raw_json) if isinstance(obj.raw_json, str) else obj.raw_json
            formatted = json.dumps(data, indent=2)
            return format_html('<pre style="max-height: 500px; overflow-y: auto;">{}</pre>', formatted)
        except:
            return "Invalid JSON"
    formatted_json.short_description = "Resume Data"
    
    def view_resume(self, obj):
        url = reverse('admin:resumes_parsedresume_change', args=[obj.id])
        return format_html('<a class="button" href="{}">View Details</a>', url)
    view_resume.short_description = "Actions"
    
    def has_add_permission(self, request):
        # Disable adding resumes through admin (should only be done through API)
        return False
    
    def has_change_permission(self, request, obj=None):
        # Allow viewing but not editing
        return request.method in ['GET', 'HEAD', 'OPTIONS']