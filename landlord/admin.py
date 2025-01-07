# landlord/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Landlord

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'phone_number', 'date_registered', 'is_verified_icon', 
                   'total_properties')
    list_filter = ('is_verified', 'date_registered')
    search_fields = ('user__username', 'user__email', 'phone_number', 'address', 
                    'company_name', 'business_license')
    date_hierarchy = 'date_registered'
    
    fieldsets = (
        ('User Information', {
            'fields': (
                'user', 
                'phone_number', 
                'address'
            )
        }),
        ('Business Information', {
            'fields': (
                'company_name', 
                'business_license', 
                'total_properties'
            )
        }),
        ('Status', {
            'fields': ('is_verified',),
            'description': 'Verification status affects landlord privileges'
        }),
        ('Registration Details', {
            'fields': ('date_registered',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('date_registered',)
    
    def display_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user.first_name else obj.user.username
    display_name.short_description = 'Name'
    
    def is_verified_icon(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    is_verified_icon.short_description = 'Verified'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('date_registered',)
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.total_properties = 0  # Set default value for new landlords
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Optional: Register any additional related models if you have them
# For example, if you have a Property model:
# @admin.register(Property)
# class PropertyAdmin(admin.ModelAdmin):
#     list_display = ('name', 'landlord', 'address', 'available')
#     list_filter = ('available', 'property_type')
#     search_fields = ('name', 'address', 'landlord__user__username')