from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'rating', 'comment', 'created_at','country')  # Added 'comment'
    search_fields = ('user__username', 'email', 'rating')  # Search by username, email, and rating
    list_filter = ('rating', 'created_at')  # Filter by rating and date
    ordering = ('-created_at',)  # Sort by newest feedback first
