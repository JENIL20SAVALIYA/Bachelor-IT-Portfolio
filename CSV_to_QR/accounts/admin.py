# accounts/admin.py
from django.contrib import admin
from .models import UserProfile, QRCode

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ('user', 'full_name', 'created_at')
    search_fields = ('user__username', 'full_name')

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    """
    Admin interface for QRCode model.
    """
    list_display = ('name', 'created_at')
    search_fields = ('name',)
