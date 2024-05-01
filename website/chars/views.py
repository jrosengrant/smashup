from django.shortcuts import render
from django.template import loader
from .models import Character

def index(request):
  chars = Character.objects.all()
  char_fields = Character._meta.get_fields()
  return render(request, "chars/index.html", {"chars": chars, "char_fields": char_fields})
