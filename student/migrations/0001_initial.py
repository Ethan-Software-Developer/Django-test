# Generated by Django 3.1.12 on 2025-01-07 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('landlord', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UniversityRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university_name', models.CharField(max_length=200)),
                ('program', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('university_student_id', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('documents', models.FileField(blank=True, null=True, upload_to='university_docs/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_university_registrations', to='landlord.landlord')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university_registrations', to='student.student')),
            ],
            options={
                'verbose_name': 'University Registration',
                'verbose_name_plural': 'University Registrations',
                'ordering': ['-submitted_at'],
            },
        ),
        migrations.CreateModel(
            name='RoomRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('single', 'Single Room'), ('double', 'Double Room'), ('studio', 'Studio Apartment')], max_length=20)),
                ('move_in_date', models.DateField()),
                ('duration', models.IntegerField(help_text='Duration in months')),
                ('budget', models.DecimalField(decimal_places=2, max_digits=8)),
                ('special_requirements', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_room_requests', to='landlord.landlord')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_requests', to='student.student')),
            ],
            options={
                'verbose_name': 'Room Request',
                'verbose_name_plural': 'Room Requests',
                'ordering': ['-submitted_at'],
            },
        ),
    ]
