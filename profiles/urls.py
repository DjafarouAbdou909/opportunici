from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload-cv/', views.upload_cv_view, name='upload_cv'),
    path('score/', views.score_detail_view, name='score_detail'),
    path('<str:username>/', views.public_profile_view, name='public_profile'),
]