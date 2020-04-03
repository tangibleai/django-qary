from rest_framework.routers import SimpleRouter

from app import views
from django.urls import path

urlpatterns = [
    path('', views.test_connection, name = 'connection'),
    path('search/', views.search_index, name = "search"),
]
