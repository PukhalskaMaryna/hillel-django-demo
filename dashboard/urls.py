# dashboard/urls.py
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.hello, name='hello'),
    path('api/ping/', views.api_ping, name='ping'),
    path('api/echo/', views.api_echo, name='echo'),
    path('files/', views.files_page, name='files'),  # ← NEW
]
