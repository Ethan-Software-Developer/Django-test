from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_registered = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'landlord_registration'
        verbose_name = 'Landlord'
        verbose_name_plural = 'Landlords'

    def __str__(self):
        return f"{self.user.get_full_name()}"

class Property(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=200)
    address = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('studio', 'Studio'),
        ('ensuite', 'Ensuite'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.room_number} - {self.get_room_type_display()}"

class RoomRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='requests')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(Landlord, on_delete=models.SET_NULL, null=True, blank=True)
    move_in_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in months")
    special_requirements = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Request for {self.room} by {self.student.get_full_name()}"
