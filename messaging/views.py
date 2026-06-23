from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Conversation, Message

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from .models import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message

from django.http import JsonResponse

@login_required
def get_messages(request, conversation_id):

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id
    )

    messages = []

    for msg in conversation.messages.all():

        messages.append({
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.username,
            "is_me": msg.sender == request.user,
            "is_read": msg.is_read,
            "time": msg.timestamp.strftime("%I:%M %p")
        })

    return JsonResponse(messages, safe=False)
    
@login_required
def chat_view(request, conversation_id):

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id
    )

    # Mark received messages as read
    conversation.messages.exclude(
        sender=request.user
    ).update(is_read=True)

    # User on the other side of the chat
    other_user = conversation.participants.exclude(
        id=request.user.id
    ).first()

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

        return redirect(
            "messaging:chat",
            conversation_id=conversation.id
        )

    return render(
        request,
        "messaging/chat.html",
        {
            "conversation": conversation,
            "other_user": other_user,
        }
    )
    
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        conversation.participants.add(other_user)

    return redirect("messaging:chat", conversation.id)

class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'messaging/conversation_list.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Message.objects.filter(
            conversation__participants=self.request.user,
            is_read=False
        ).exclude(sender=self.request.user).count()
        return context

class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'messaging/conversation_detail.html'
    context_object_name = 'conversation'
    pk_url_kwarg = 'conversation_id'

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all()
        # Mark messages as read
        self.object.messages.filter(is_read=False).exclude(sender=self.request.user).update(is_read=True)
        return context

class StartConversationView(LoginRequiredMixin, View):
    def post(self, request, username):
        other_user = get_object_or_404(User, username=username)
        
        # Check if conversation already exists
        conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, other_user)
        
        return redirect('messaging:detail', conversation_id=conversation.id)

class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        content = request.POST.get('content')
        
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Update conversation timestamp
            conversation.save()
        
        return redirect('messaging:detail', conversation_id=conversation.id)

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(
        Message,
        id=message_id,
        sender=request.user
    )

    conversation_id = message.conversation.id

    message.delete()

    return redirect(
        "messaging:chat",
        conversation_id=conversation_id
    )

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(
        Message,
        id=message_id,
        sender=request.user
    )

    if request.method == "POST":
        message.content = request.POST.get("content")
        message.save()

        return redirect(
            "messaging:chat",
            conversation_id=message.conversation.id
        )

    return render(
        request,
        "messaging/edit_message.html",
        {"message": message}
    )
