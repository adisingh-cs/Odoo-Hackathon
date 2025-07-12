from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Announcement
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.location = request.POST.get('location', '')
        user.availability = request.POST.get('availability', '')
        user.is_private = 'is_private' in request.POST
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']
        user.save()
        return redirect('profile')
    return render(request, 'profile.html')

from .models import Feedback, Skill, Swap

@login_required
def skill_list(request):
    skills = Skill.objects.filter(user=request.user)
    return render(request, 'skill_list.html', {'skills': skills})

@login_required
def add_skill(request):
    if request.method == 'POST':
        Skill.objects.create(
            user=request.user,
            name=request.POST['name'],
            skill_type=request.POST['skill_type'],
            description=request.POST.get('description', ''),
            tags=request.POST.get('tags', '')
        )
        return redirect('skill_list')
    return render(request, 'add_skill.html')

@login_required
def edit_skill(request, skill_id):
    skill = Skill.objects.get(id=skill_id, user=request.user)
    if request.method == 'POST':
        skill.name = request.POST['name']
        skill.skill_type = request.POST['skill_type']
        skill.description = request.POST.get('description', '')
        skill.tags = request.POST.get('tags', '')
        skill.save()
        return redirect('skill_list')
    return render(request, 'edit_skill.html', {'skill': skill})

@login_required
def delete_skill(request, skill_id):
    Skill.objects.filter(id=skill_id, user=request.user).delete()
    return redirect('skill_list')

def search(request):
    query = request.GET.get('q', '').strip()
    if query:
        skills = Skill.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        ).exclude(user__is_private=True)
    else:
        skills = Skill.objects.none()
    return render(request, 'search.html', {'skills': skills, 'query': query})

@login_required
def create_swap(request, skill_id):
    skill = Skill.objects.get(id=skill_id)
    if request.method == 'POST':
        Swap.objects.create(
            requester=request.user,
            recipient=skill.user,
            skill=skill,
            message=request.POST.get('message', ''),
            status=Swap.PENDING
        )
        return redirect('swap_inbox')
    return render(request, 'create_swap.html', {'skill': skill})

@login_required
def swap_inbox(request):
    received = request.user.received_swaps.all()
    sent = request.user.sent_swaps.all()
    return render(request, 'swap_inbox.html', {'received': received, 'sent': sent})

@login_required
def update_swap(request, swap_id, action):
    swap = Swap.objects.get(id=swap_id, recipient=request.user)
    if action == 'accept':
        swap.status = Swap.ACCEPTED
    elif action == 'reject':
        swap.status = Swap.REJECTED
    swap.save()
    return redirect('swap_inbox')

@login_required
def leave_feedback(request, swap_id):
    swap = Swap.objects.get(id=swap_id)
    if request.method == 'POST':
        Feedback.objects.create(
            swap=swap,
            rating=request.POST['rating'],
            comment=request.POST.get('comment', ''),
            reviewer=request.user,
            reviewee=swap.recipient if request.user == swap.requester else swap.requester
        )
        swap.status = Swap.COMPLETED
        swap.save()
        return redirect('swap_inbox')
    return render(request, 'leave_feedback.html', {'swap': swap})

def home(request):
    announcements = Announcement.objects.filter(is_active=True)
    return render(request, 'home.html', {'announcements': announcements})

