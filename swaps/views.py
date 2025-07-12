from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import SwapRequest, SwapTransaction, SwapReview
from .forms import SwapRequestForm, SwapReviewForm, SwapTransactionForm
from skills.models import SkillListing
from users.models import Notification


@login_required
def swap_request_create(request, skill_id):
    """Create a new swap request."""
    skill = get_object_or_404(SkillListing, id=skill_id, is_active=True, skill_type='offer')
    
    # Check if user is trying to swap with themselves
    if skill.user == request.user:
        messages.error(request, 'You cannot create a swap request for your own skill.')
        return redirect('skills:skill_detail', skill_id=skill.id)
    
    # Check if there's already a pending request
    existing_request = SwapRequest.objects.filter(
        requesting_user=request.user,
        requesting_skill=skill,
        status='pending'
    ).first()
    
    if existing_request:
        messages.warning(request, 'You already have a pending swap request for this skill.')
        return redirect('swaps:swap_detail', swap_id=existing_request.id)
    
    if request.method == 'POST':
        form = SwapRequestForm(request.POST, requesting_skill=skill)
        if form.is_valid():
            swap_request = form.save(commit=False)
            swap_request.requesting_user = request.user
            swap_request.requested_user = skill.user
            swap_request.requesting_skill = skill
            swap_request.save()
            
            # Create notification for the requested user
            Notification.objects.create(
                user=skill.user,
                notification_type='swap_request',
                title='New Swap Request',
                message=f'{request.user.get_full_name()} wants to swap skills with you.',
                related_object_id=swap_request.id,
                related_object_type='SwapRequest'
            )
            
            messages.success(request, 'Swap request sent successfully!')
            return redirect('swaps:swap_detail', swap_id=swap_request.id)
    else:
        form = SwapRequestForm(requesting_skill=skill)
    
    context = {
        'form': form,
        'skill': skill,
    }
    return render(request, 'swaps/swap_request_form.html', context)


@login_required
def swap_list(request):
    """List user's swap requests."""
    # Get all swap requests where user is involved
    swap_requests = SwapRequest.objects.filter(
        Q(requesting_user=request.user) | Q(requested_user=request.user)
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(swap_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'swaps/swap_list.html', context)


@login_required
def swap_detail(request, swap_id):
    """View a specific swap request."""
    swap_request = get_object_or_404(
        SwapRequest, 
        Q(requesting_user=request.user) | Q(requested_user=request.user),
        id=swap_id
    )
    
    # Check if user can review this swap
    can_review = False
    if swap_request.status == 'completed':
        can_review = not SwapReview.objects.filter(
            swap_request=swap_request,
            reviewer=request.user
        ).exists()
    
    # Handle review submission
    if request.method == 'POST' and can_review:
        review_form = SwapReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.swap_request = swap_request
            review.reviewer = request.user
            review.reviewed_user = swap_request.requested_user if request.user == swap_request.requesting_user else swap_request.requesting_user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('swaps:swap_detail', swap_id=swap_request.id)
    else:
        review_form = SwapReviewForm()
    
    context = {
        'swap_request': swap_request,
        'can_review': can_review,
        'review_form': review_form,
    }
    return render(request, 'swaps/swap_detail.html', context)


@login_required
def swap_accept(request, swap_id):
    """Accept a swap request."""
    swap_request = get_object_or_404(SwapRequest, id=swap_id, requested_user=request.user, status='pending')
    
    if request.method == 'POST':
        swap_request.status = 'accepted'
        swap_request.save()
        
        # Create notification for the requesting user
        Notification.objects.create(
            user=swap_request.requesting_user,
            notification_type='swap_accepted',
            title='Swap Request Accepted',
            message=f'{request.user.get_full_name()} accepted your swap request.',
            related_object_id=swap_request.id,
            related_object_type='SwapRequest'
        )
        
        messages.success(request, 'Swap request accepted!')
        return redirect('swaps:swap_detail', swap_id=swap_request.id)
    
    return redirect('swaps:swap_detail', swap_id=swap_request.id)


@login_required
def swap_reject(request, swap_id):
    """Reject a swap request."""
    swap_request = get_object_or_404(SwapRequest, id=swap_id, requested_user=request.user, status='pending')
    
    if request.method == 'POST':
        swap_request.status = 'rejected'
        swap_request.save()
        
        # Create notification for the requesting user
        Notification.objects.create(
            user=swap_request.requesting_user,
            notification_type='swap_rejected',
            title='Swap Request Rejected',
            message=f'{request.user.get_full_name()} rejected your swap request.',
            related_object_id=swap_request.id,
            related_object_type='SwapRequest'
        )
        
        messages.success(request, 'Swap request rejected.')
        return redirect('swaps:swap_list')
    
    return redirect('swaps:swap_detail', swap_id=swap_request.id)


@login_required
def swap_complete(request, swap_id):
    """Mark a swap as completed."""
    swap_request = get_object_or_404(
        SwapRequest, 
        Q(requesting_user=request.user) | Q(requested_user=request.user),
        id=swap_id, 
        status='accepted'
    )
    
    if request.method == 'POST':
        form = SwapTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.swap_request = swap_request
            transaction.save()
            
            swap_request.status = 'completed'
            swap_request.completed_at = timezone.now()
            swap_request.save()
            
            # Update user swap counts
            swap_request.requesting_user.total_swaps += 1
            swap_request.requesting_user.save()
            swap_request.requested_user.total_swaps += 1
            swap_request.requested_user.save()
            
            messages.success(request, 'Swap marked as completed!')
            return redirect('swaps:swap_detail', swap_id=swap_request.id)
    else:
        form = SwapTransactionForm()
    
    context = {
        'form': form,
        'swap_request': swap_request,
    }
    return render(request, 'swaps/swap_complete_form.html', context)


@login_required
def swap_cancel(request, swap_id):
    """Cancel a swap request."""
    swap_request = get_object_or_404(
        SwapRequest, 
        id=swap_id, 
        requesting_user=request.user,
        status='pending'
    )
    
    if request.method == 'POST':
        swap_request.status = 'cancelled'
        swap_request.save()
        messages.success(request, 'Swap request cancelled.')
        return redirect('swaps:swap_list')
    
    return redirect('swaps:swap_detail', swap_id=swap_request.id)


@login_required
def sent_requests(request):
    """View sent swap requests."""
    requests = SwapRequest.objects.filter(requesting_user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'swaps/sent_requests.html', context)


@login_required
def received_requests(request):
    """View received swap requests."""
    requests = SwapRequest.objects.filter(requested_user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'swaps/received_requests.html', context) 