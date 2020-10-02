from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

def home_view(request):
    return render(request, 'notifications/home.html', {})




