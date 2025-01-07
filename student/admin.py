# student/admin.py
from django.contrib import admin
from .models import Student, UniversityRegistration, RoomRequest

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_joined')
    search_fields = ('user__username', 'user__email', 'phone_number')
    date_hierarchy = 'date_joined'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number')
        }),
        ('Account Details', {
            'fields': ('date_joined',)
        })
    )

@admin.register(UniversityRegistration)
class UniversityRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'university_name', 'program', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('student__user__username', 'university_name', 'program', 'email')
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'university_student_id')
        }),
        ('University Details', {
            'fields': ('university_name', 'program', 'start_date')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'email')
        }),
        ('Documentation', {
            'fields': ('documents',)
        }),
        ('Status Information', {
            'fields': ('status', 'notes')
        }),
        ('Review Details', {
            'fields': ('reviewed_by', 'reviewed_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('submitted_at', 'reviewed_at')

@admin.register(RoomRequest)
class RoomRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'room_type', 'move_in_date', 'budget', 'status', 'submitted_at')
    list_filter = ('status', 'room_type', 'submitted_at')
    search_fields = ('student__user__username', 'special_requirements')
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Room Details', {
            'fields': ('room_type', 'move_in_date', 'duration', 'budget')
        }),
        ('Additional Information', {
            'fields': ('special_requirements',)
        }),
        ('Status Information', {
            'fields': ('status', 'notes')
        }),
        ('Review Details', {
            'fields': ('reviewed_by', 'reviewed_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('submitted_at', 'reviewed_at')