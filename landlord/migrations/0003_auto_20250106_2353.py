# Generated by Django 3.1.12 on 2025-01-07 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landlord', '0002_auto_20250106_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=50)),
                ('room_type', models.CharField(choices=[('single', 'Single Room'), ('double', 'Double Room'), ('studio', 'Studio'), ('ensuite', 'Ensuite')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_available', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='landlord.property')),
            ],
        ),
        migrations.RemoveField(
            model_name='landlord',
            name='business_license',
        ),
        migrations.RemoveField(
            model_name='landlord',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='landlord',
            name='total_properties',
        ),
        migrations.AlterField(
            model_name='landlord',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='landlord',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.CreateModel(
            name='RoomRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('move_in_date', models.DateField()),
                ('duration', models.IntegerField(help_text='Duration in months')),
                ('special_requirements', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='landlord.landlord')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='landlord.room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='landlord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='landlord.landlord'),
        ),
    ]
