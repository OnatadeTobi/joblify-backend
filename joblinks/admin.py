from django.contrib import admin
from .models import JobLink

@admin.register(JobLink)
class JobLinkAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('title', 'company', 'platform', 'location', 'job_type', 'pay', 'user', 'created_at')
    
    # Add filters on the right side
    list_filter = ('platform', 'job_type', 'location', 'created_at')
    
    # Add search functionality
    search_fields = ('title', 'company', 'platform', 'location')
    
    # Add date hierarchy for created_at
    date_hierarchy = 'created_at'
    
    # Fields to show in the detail view
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'company', 'platform')
        }),
        ('Job Details', {
            'fields': ('location', 'job_type', 'pay')
        }),
        ('User Information', {
            'fields': ('user', 'created_at')
        }),
    )
    
    # Make certain fields read-only
    readonly_fields = ('created_at',)
    
    # Add actions for bulk operations
    actions = ['mark_as_remote', 'mark_as_hybrid', 'mark_as_onsite']
    
    def mark_as_remote(self, request, queryset):
        queryset.update(job_type='Remote')
    mark_as_remote.short_description = "Mark selected jobs as Remote"
    
    def mark_as_hybrid(self, request, queryset):
        queryset.update(job_type='Hybrid')
    mark_as_hybrid.short_description = "Mark selected jobs as Hybrid"
    
    def mark_as_onsite(self, request, queryset):
        queryset.update(job_type='On-site')
    mark_as_onsite.short_description = "Mark selected jobs as On-site"
    
    # Add list per page option
    list_per_page = 20
    
    # Add ordering
    ordering = ('-created_at',)