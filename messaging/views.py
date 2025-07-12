from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Conversation, Message, PlatformMessage, UserMessageRead
from .forms import MessageForm, PlatformMessageForm
from users.models import Notification


@login_required
def conversation_list(request):
    """List user's conversations."""
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    
    # Pagination
    paginator = Paginator(conversations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'messaging/conversation_list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """View a specific conversation."""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    # Handle new message submission
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Update conversation timestamp
            conversation.save()
            
            # Create notification for other participants
            other_participants = conversation.participants.exclude(id=request.user.id)
            for participant in other_participants:
                Notification.objects.create(
                    user=participant,
                    notification_type='message',
                    title='New Message',
                    message=f'{request.user.get_full_name()} sent you a message.',
                    related_object_id=conversation.id,
                    related_object_type='Conversation'
                )
            
            return redirect('messaging:conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    # Get messages with pagination
    message_list = conversation.messages.all()
    paginator = Paginator(message_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'conversation': conversation,
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def start_conversation(request, user_id):
    """Start a new conversation with a user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    other_user = get_object_or_404(User, id=user_id, is_active=True)
    
    if other_user == request.user:
        messages.error(request, 'You cannot start a conversation with yourself.')
        return redirect('users:user_list')
    
    # Check if conversation already exists
    existing_conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if existing_conversation:
        return redirect('messaging:conversation_detail', conversation_id=existing_conversation.id)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)


@login_required
def platform_messages(request):
    """View platform messages/announcements."""
    platform_messages = PlatformMessage.objects.filter(is_active=True).order_by('-created_at')
    
    # Mark messages as read
    unread_messages = platform_messages.exclude(read_by__user=request.user)
    for message in unread_messages:
        UserMessageRead.objects.get_or_create(user=request.user, platform_message=message)
    
    # Pagination
    paginator = Paginator(platform_messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'messaging/platform_messages.html', context)


@login_required
def platform_message_detail(request, message_id):
    """View a specific platform message."""
    platform_message = get_object_or_404(PlatformMessage, id=message_id, is_active=True)
    
    # Mark as read
    UserMessageRead.objects.get_or_create(user=request.user, platform_message=platform_message)
    
    context = {
        'platform_message': platform_message,
    }
    return render(request, 'messaging/platform_message_detail.html', context)


@login_required
def mark_conversation_read(request, conversation_id):
    """Mark all messages in a conversation as read."""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)


@login_required
def get_unread_count(request):
    """Get unread message count for AJAX requests."""
    # Count unread messages in conversations
    unread_conversations = Conversation.objects.filter(
        participants=request.user,
        messages__is_read=False
    ).exclude(messages__sender=request.user).distinct().count()
    
    # Count unread platform messages
    unread_platform = PlatformMessage.objects.filter(
        is_active=True
    ).exclude(read_by__user=request.user).count()
    
    total_unread = unread_conversations + unread_platform
    
    return JsonResponse({'count': total_unread})


# Admin views for platform messages
@login_required
def create_platform_message(request):
    """Create a new platform message (admin only)."""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create platform messages.')
        return redirect('messaging:platform_messages')
    
    if request.method == 'POST':
        form = PlatformMessageForm(request.POST)
        if form.is_valid():
            platform_message = form.save(commit=False)
            platform_message.created_by = request.user
            platform_message.save()
            
            # Create notifications for all users
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users = User.objects.filter(is_active=True)
            
            for user in users:
                Notification.objects.create(
                    user=user,
                    notification_type='announcement',
                    title=platform_message.title,
                    message=platform_message.content[:100] + '...' if len(platform_message.content) > 100 else platform_message.content,
                    related_object_id=platform_message.id,
                    related_object_type='PlatformMessage'
                )
            
            messages.success(request, 'Platform message created successfully!')
            return redirect('messaging:platform_messages')
    else:
        form = PlatformMessageForm()
    
    context = {
        'form': form,
        'title': 'Create Platform Message',
    }
    return render(request, 'messaging/platform_message_form.html', context) 