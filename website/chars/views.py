from django.shortcuts import render
from django.template import loader
from .models import Character

def index(request):
  chars = Character.objects.all()
  return render(request, "chars/index.html", {"chars": chars})
