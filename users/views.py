from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm, UserSearchForm
from .models import UserProfile, Notification
from skills.models import SkillListing
from swaps.models import SwapRequest
from messaging.models import Conversation


def home(request):
    """Home page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Show some featured skill listings for non-authenticated users
    featured_skills = SkillListing.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    context = {
        'featured_skills': featured_skills,
    }
    return render(request, 'users/home.html', context)


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to SkillExchange.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard view."""
    user = request.user
    
    # Get user's skill listings
    user_skills = SkillListing.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get recent swap requests
    received_requests = SwapRequest.objects.filter(requested_user=user, status='pending').order_by('-created_at')[:5]
    sent_requests = SwapRequest.objects.filter(requesting_user=user).order_by('-created_at')[:5]
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')[:5]
    
    # Get recent conversations
    conversations = Conversation.objects.filter(participants=user).order_by('-updated_at')[:5]
    
    context = {
        'user_skills': user_skills,
        'received_requests': received_requests,
        'sent_requests': sent_requests,
        'unread_notifications': unread_notifications,
        'conversations': conversations,
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def profile(request):
    """User profile view."""
    user = request.user
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)
    
    # Get user's skill listings
    skill_listings = SkillListing.objects.filter(user=user).order_by('-created_at')
    
    # Get user's swap history
    swap_requests = SwapRequest.objects.filter(
        Q(requesting_user=user) | Q(requested_user=user)
    ).order_by('-created_at')
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'skill_listings': skill_listings,
        'swap_requests': swap_requests,
    }
    return render(request, 'users/profile.html', context)


@login_required
def user_list(request):
    """List all users with search and filtering."""
    form = UserSearchForm(request.GET)
    users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        location = form.cleaned_data.get('location')
        min_rating = form.cleaned_data.get('min_rating')
        verified_only = form.cleaned_data.get('verified_only')
        
        if query:
            users = users.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(location__icontains=query)
            )
        
        if location:
            users = users.filter(location__icontains=location)
        
        if min_rating:
            users = users.filter(rating__gte=min_rating)
        
        if verified_only:
            users = users.filter(is_verified=True)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'users/user_list.html', context)


@login_required
def user_detail(request, user_id):
    """View another user's profile."""
    user = get_object_or_404(User, id=user_id, is_active=True)
    
    if user == request.user:
        return redirect('profile')
    
    # Get user's public skill listings
    skill_listings = SkillListing.objects.filter(user=user, is_active=True).order_by('-created_at')
    
    # Check if there's an existing conversation
    existing_conversation = Conversation.objects.filter(participants=request.user).filter(participants=user).first()
    
    context = {
        'profile_user': user,
        'skill_listings': skill_listings,
        'existing_conversation': existing_conversation,
    }
    return render(request, 'users/user_detail.html', context)


@login_required
def notifications(request):
    """User notifications view."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'users/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, 'Notification marked as read.')
    return redirect('notifications')


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications')


@login_required
def get_unread_count(request):
    """Get unread notification count for AJAX requests."""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count}) 