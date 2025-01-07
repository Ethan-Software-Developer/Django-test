
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .forms import LandlordRegistrationForm
from .models import Landlord, Property, Room, RoomRequest

SECURITY_KEY = "LANDLORD2024"

def landlord_register(request):
    # First, log out any existing user
    logout(request)
    
    if request.method == 'POST':
        form = LandlordRegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                # The form's save method will handle name splitting and email as username
                user = form.save(commit=False)
                
                # Check if username/email already exists
                if User.objects.filter(username=user.email).exists():
                    messages.error(request, 'An account with this email already exists.')
                    return render(request, 'landlord/register.html', {'form': form})
                
                # If all is well, save the user
                user.save()
                
                # Create the landlord profile
                Landlord.objects.create(user=user)
                
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('landlord-login')
                
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
    else:
        form = LandlordRegistrationForm()
    
    return render(request, 'landlord/register.html', {'form': form})

def landlord_login(request):
    # First, log out any existing user
    logout(request)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            try:
                # Try to authenticate with email as username
                user = authenticate(username=email, password=password)
                if user is not None:
                    # Check if user has a landlord profile
                    if hasattr(user, 'landlord'):
                        login(request, user)
                        messages.success(request, 'Successfully logged in!')
                        return redirect('landlord_dashboard')
                    else:
                        messages.error(request, 'This account does not have landlord privileges.')
                else:
                    messages.error(request, 'Invalid email or password.')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please enter both email and password.')
            
    return render(request, 'landlord/login.html')

@login_required
def landlord_dashboard(request):
    if not hasattr(request.user, 'landlord'):
        logout(request)
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    landlord = request.user.landlord
    
    # Get all properties for this landlord
    properties = Property.objects.filter(landlord=landlord)
    
    # Get all rooms across all properties
    rooms = Room.objects.filter(property__landlord=landlord)
    
    # Get pending requests
    pending_requests = RoomRequest.objects.filter(
        room__property__landlord=landlord,
        status='pending'
    ).order_by('-submitted_at')
    
    # Get processed requests
    processed_requests = RoomRequest.objects.filter(
        room__property__landlord=landlord
    ).exclude(status='pending').order_by('-reviewed_at')
    
    context = {
        'landlord': landlord,
        'properties': properties,
        'total_properties': properties.count(),
        'total_rooms': rooms.count(),
        'available_rooms': rooms.filter(is_available=True).count(),
        'pending_requests': pending_requests,
        'processed_requests': processed_requests,
        'pending_count': pending_requests.count(),
    }
    
    return render(request, 'landlord/dashboard.html', context)

@login_required
def property_list(request):
    if not hasattr(request.user, 'landlord'):
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    properties = Property.objects.filter(landlord=request.user.landlord)
    return render(request, 'landlord/property_list.html', {'properties': properties})

@login_required
def property_detail(request, property_id):
    if not hasattr(request.user, 'landlord'):
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    property = get_object_or_404(Property, id=property_id, landlord=request.user.landlord)
    rooms = Room.objects.filter(property=property)
    
    context = {
        'property': property,
        'rooms': rooms,
        'total_rooms': rooms.count(),
        'available_rooms': rooms.filter(is_available=True).count(),
    }
    
    return render(request, 'landlord/property_detail.html', context)

@login_required
def process_request(request, request_id):
    if not hasattr(request.user, 'landlord'):
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    if request.method == 'POST':
        try:
            room_request = get_object_or_404(
                RoomRequest,
                id=request_id,
                room__property__landlord=request.user.landlord
            )
            action = request.POST.get('action')
            notes = request.POST.get('notes', '')
            
            if action in ['accept', 'decline']:
                room_request.status = 'accepted' if action == 'accept' else 'declined'
                room_request.reviewed_at = timezone.now()
                room_request.reviewed_by = request.user.landlord
                room_request.notes = notes
                
                if action == 'accept':
                    # Update room availability
                    room_request.room.is_available = False
                    room_request.room.save()
                
                room_request.save()
                
                messages.success(
                    request, 
                    f'Room request has been {room_request.status}.'
                )
            else:
                messages.error(request, 'Invalid action specified.')
        except RoomRequest.DoesNotExist:
            messages.error(request, 'Room request not found.')
        except Exception as e:
            messages.error(request, str(e))
    
    return redirect('landlord_dashboard')

@login_required
def profile_settings(request):
    if not hasattr(request.user, 'landlord'):
        logout(request)
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    if request.method == 'POST':
        try:
            landlord = request.user.landlord
            landlord.phone_number = request.POST.get('phone_number', '')
            landlord.address = request.POST.get('address', '')
            landlord.save()
            
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Failed to update profile: {str(e)}')
    
    return render(request, 'landlord/profile_settings.html', {'landlord': request.user.landlord})

@login_required
def landlord_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('landlord-login')