from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import SkillListing, SkillReview, Category
from .forms import SkillListingForm, SkillReviewForm, SkillSearchForm


def skill_list(request):
    """List all skill listings with search and filtering."""
    form = SkillSearchForm(request.GET)
    skills = SkillListing.objects.filter(is_active=True, status='active')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        skill_type = form.cleaned_data.get('skill_type')
        difficulty_level = form.cleaned_data.get('difficulty_level')
        min_rating = form.cleaned_data.get('min_rating')
        
        if query:
            skills = skills.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__contains=[query]) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )
        
        if category:
            skills = skills.filter(category=category)
        
        if skill_type:
            skills = skills.filter(skill_type=skill_type)
        
        if difficulty_level:
            skills = skills.filter(difficulty_level=difficulty_level)
        
        if min_rating:
            skills = skills.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)
    
    # Pagination
    paginator = Paginator(skills, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for sidebar
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'skills/skill_list.html', context)


@login_required
def skill_create(request):
    """Create a new skill listing."""
    if request.method == 'POST':
        form = SkillListingForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill listing created successfully!')
            return redirect('skills:skill_detail', skill_id=skill.id)
    else:
        form = SkillListingForm()
    
    context = {
        'form': form,
        'title': 'Create Skill Listing',
    }
    return render(request, 'skills/skill_form.html', context)


def skill_detail(request, skill_id):
    """View a specific skill listing."""
    skill = get_object_or_404(SkillListing, id=skill_id, is_active=True)
    reviews = skill.reviews.all()
    
    # Check if user has already reviewed this skill
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(reviewer=request.user).first()
    
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = SkillReviewForm(request.POST)
        if review_form.is_valid():
            # Check if user already reviewed
            if user_review:
                messages.error(request, 'You have already reviewed this skill.')
            else:
                review = review_form.save(commit=False)
                review.skill_listing = skill
                review.reviewer = request.user
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('skills:skill_detail', skill_id=skill.id)
    else:
        review_form = SkillReviewForm()
    
    context = {
        'skill': skill,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
    }
    return render(request, 'skills/skill_detail.html', context)


@login_required
def skill_edit(request, skill_id):
    """Edit a skill listing."""
    skill = get_object_or_404(SkillListing, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        form = SkillListingForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill listing updated successfully!')
            return redirect('skills:skill_detail', skill_id=skill.id)
    else:
        form = SkillListingForm(instance=skill)
    
    context = {
        'form': form,
        'skill': skill,
        'title': 'Edit Skill Listing',
    }
    return render(request, 'skills/skill_form.html', context)


@login_required
def skill_delete(request, skill_id):
    """Delete a skill listing."""
    skill = get_object_or_404(SkillListing, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill listing deleted successfully!')
        return redirect('skills:my_skills')
    
    context = {
        'skill': skill,
    }
    return render(request, 'skills/skill_confirm_delete.html', context)


@login_required
def my_skills(request):
    """View user's own skill listings."""
    skills = SkillListing.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(skills, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'skills/my_skills.html', context)


@login_required
def skill_toggle_status(request, skill_id):
    """Toggle skill listing active status."""
    skill = get_object_or_404(SkillListing, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        skill.is_active = not skill.is_active
        skill.save()
        
        status = 'activated' if skill.is_active else 'deactivated'
        messages.success(request, f'Skill listing {status} successfully!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'is_active': skill.is_active})
    
    return redirect('skills:my_skills')


@login_required
def skill_reviews(request, skill_id):
    """View all reviews for a skill listing."""
    skill = get_object_or_404(SkillListing, id=skill_id)
    reviews = skill.reviews.all()
    
    # Pagination
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'skill': skill,
        'page_obj': page_obj,
    }
    return render(request, 'skills/skill_reviews.html', context)


def category_detail(request, category_id):
    """View skill listings by category."""
    category = get_object_or_404(Category, id=category_id)
    skills = SkillListing.objects.filter(category=category, is_active=True, status='active')
    
    # Pagination
    paginator = Paginator(skills, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'skills/category_detail.html', context) 