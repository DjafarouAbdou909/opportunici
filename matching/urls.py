from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('career-gap/', views.career_gap_view, name='career_gap'),
]