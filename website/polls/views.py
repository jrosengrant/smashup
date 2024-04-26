from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Question

## with shortcut
def index(request):
  latest_question_list = Question.objects.order_by("pub_date")[:5]
  context = {
    "latest_question_list": latest_question_list
  }
  return render(request, "polls/index.html", context)

## without shortcut
# def index(request):
#   latest_question_list = Question.objects.order_by("pub_date")[:5]
#   template = loader.get_template("polls/index.html")
#   context = {
#     "latest_question_list": latest_question_list
#   }
#   return HttpResponse(template.render(context, request))

###v3 shortcut
def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, "polls/detail.html", {"question": question})
# ###v2
# def detail(request, question_id):
#   try:
#     question = Question.objects.get(pk=question_id)
#   except Question.DoesNotExist:
#     raise Http404("Question does not exist")
#   return render(request, "polls/detail.html", {"question": question})
###v1
# def detail(request, question_id):
#   return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
  return HttpResponse("You're looking at the results of question %s." % question_id)

def vote(request, question_id):
  return HttpResponse("You're voting on question %s." % question_id)