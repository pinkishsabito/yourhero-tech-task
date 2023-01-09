from django.urls import path
from . import views

urlpatterns = [
    path('word_cloud/', views.word_cloud),
]
