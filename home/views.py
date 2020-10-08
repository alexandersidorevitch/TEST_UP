from django.shortcuts import render

# Create your views here.
from topic.models import Topics


def home(request):
    topics = Topics.objects.all()
    return render(request, 'landing/home.html', locals())
