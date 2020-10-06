from django.shortcuts import render
from .models import Conversation, Message


# Create your views here.

def home_view(request):
    context = {}
    conversation = Conversation.objects.get(name='test')
    messages = Message.objects.filter(conversation=conversation)
    context['messages'] = messages
    return render(request, 'notifications/home.html', context)




