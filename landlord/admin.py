# landlord/admin.py
from django.contrib import admin
from .models import Landlord

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    def total_properties(self, obj):
        return obj.properties.count()  # Assuming you have a related_name='properties' in your Property model
    
    total_properties.short_description = "Total Properties"

    list_display = ('user', 'phone_number', 'date_registered', 'is_verified', 'total_properties')
    list_filter = ('is_verified', 'date_registered')
    search_fields = ('user__username', 'user__email', 'phone_number', 'address')
    date_hierarchy = 'date_registered'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'address')
        }),
        ('Business Information', {
            'fields': ('company_name', 'business_license')  # Removed total_properties from here
        }),
        ('Status', {
            'fields': ('is_verified',)
        })
    )