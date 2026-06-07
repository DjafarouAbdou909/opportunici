from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.opportunities_list_view, name='list'),
]