from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Report, Analytics, UserActivity
from .forms import ReportForm, ReportAdminForm
from users.models import User
from skills.models import SkillListing
from swaps.models import SwapRequest
from messaging.models import Message


@login_required
def report_create(request):
    """Create a new report."""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            
            # Log activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='report_filed',
                description=f'Filed report: {report.title}',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                related_object_id=report.id,
                related_object_type='Report'
            )
            
            messages.success(request, 'Report submitted successfully! We will review it shortly.')
            return redirect('reports:my_reports')
    else:
        form = ReportForm()
    
    context = {
        'form': form,
    }
    return render(request, 'reports/report_form.html', context)


@login_required
def my_reports(request):
    """View user's own reports."""
    reports = Report.objects.filter(reporter=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'reports/my_reports.html', context)


@login_required
def report_detail(request, report_id):
    """View a specific report."""
    report = get_object_or_404(Report, id=report_id, reporter=request.user)
    
    context = {
        'report': report,
    }
    return render(request, 'reports/report_detail.html', context)


# Admin views
def is_staff_user(user):
    """Check if user is staff."""
    return user.is_staff


@login_required
@user_passes_test(is_staff_user)
def admin_reports(request):
    """Admin view of all reports."""
    reports = Report.objects.all().order_by('-created_at')
    
    # Filtering
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    
    if status_filter:
        reports = reports.filter(status=status_filter)
    if type_filter:
        reports = reports.filter(report_type=type_filter)
    
    # Pagination
    paginator = Paginator(reports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
    }
    return render(request, 'reports/admin_reports.html', context)


@login_required
@user_passes_test(is_staff_user)
def admin_report_detail(request, report_id):
    """Admin view of a specific report."""
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        form = ReportAdminForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            if report.status in ['resolved', 'dismissed'] and not report.resolved_by:
                report.resolved_by = request.user
                report.resolved_at = timezone.now()
            report.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('reports:admin_reports')
    else:
        form = ReportAdminForm(instance=report)
    
    context = {
        'report': report,
        'form': form,
    }
    return render(request, 'reports/admin_report_detail.html', context)


@login_required
@user_passes_test(is_staff_user)
def analytics_dashboard(request):
    """Admin analytics dashboard."""
    # Get current date
    today = timezone.now().date()
    
    # Get analytics for today
    today_analytics, created = Analytics.objects.get_or_create(date=today)
    
    # Get recent analytics (last 30 days)
    recent_analytics = Analytics.objects.filter(
        date__gte=today - timedelta(days=30)
    ).order_by('date')
    
    # Get summary statistics
    total_users = User.objects.filter(is_active=True).count()
    total_skills = SkillListing.objects.filter(is_active=True).count()
    total_swaps = SwapRequest.objects.count()
    completed_swaps = SwapRequest.objects.filter(status='completed').count()
    pending_reports = Report.objects.filter(status='pending').count()
    
    # Get recent activity
    recent_activities = UserActivity.objects.all().order_by('-created_at')[:20]
    
    # Get top users by activity
    top_users = User.objects.annotate(
        activity_count=Count('activities')
    ).order_by('-activity_count')[:10]
    
    context = {
        'today_analytics': today_analytics,
        'recent_analytics': recent_analytics,
        'total_users': total_users,
        'total_skills': total_skills,
        'total_swaps': total_swaps,
        'completed_swaps': completed_swaps,
        'pending_reports': pending_reports,
        'recent_activities': recent_activities,
        'top_users': top_users,
    }
    return render(request, 'reports/analytics_dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def user_activity_log(request):
    """Admin view of user activity logs."""
    activities = UserActivity.objects.all().order_by('-created_at')
    
    # Filtering
    user_filter = request.GET.get('user')
    activity_filter = request.GET.get('activity')
    
    if user_filter:
        activities = activities.filter(user__email__icontains=user_filter)
    if activity_filter:
        activities = activities.filter(activity_type=activity_filter)
    
    # Pagination
    paginator = Paginator(activities, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'user_filter': user_filter,
        'activity_filter': activity_filter,
    }
    return render(request, 'reports/user_activity_log.html', context)


@login_required
@user_passes_test(is_staff_user)
def analytics_summary(request):
    """Get analytics summary for AJAX requests."""
    today = timezone.now().date()
    
    # Get today's analytics
    today_analytics, created = Analytics.objects.get_or_create(date=today)
    
    # Get yesterday's analytics for comparison
    yesterday = today - timedelta(days=1)
    yesterday_analytics = Analytics.objects.filter(date=yesterday).first()
    
    # Calculate growth
    user_growth = 0
    skill_growth = 0
    swap_growth = 0
    
    if yesterday_analytics:
        user_growth = ((today_analytics.total_users - yesterday_analytics.total_users) / yesterday_analytics.total_users * 100) if yesterday_analytics.total_users > 0 else 0
        skill_growth = ((today_analytics.total_skills - yesterday_analytics.total_skills) / yesterday_analytics.total_skills * 100) if yesterday_analytics.total_skills > 0 else 0
        swap_growth = ((today_analytics.total_swaps - yesterday_analytics.total_swaps) / yesterday_analytics.total_swaps * 100) if yesterday_analytics.total_swaps > 0 else 0
    
    data = {
        'total_users': today_analytics.total_users,
        'total_skills': today_analytics.total_skills,
        'total_swaps': today_analytics.total_swaps,
        'completed_swaps': today_analytics.completed_swaps,
        'pending_reports': today_analytics.pending_reports,
        'user_growth': round(user_growth, 1),
        'skill_growth': round(skill_growth, 1),
        'swap_growth': round(swap_growth, 1),
    }
    
    return JsonResponse(data) 