from django.urls import path

from . import views

app_name = "chars"
urlpatterns = [
    path("", views.index, name="index")
]