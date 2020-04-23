from elastic_app import views
from django.urls import path


urlpatterns = [
    path('connect/', views.test_connection, name='connection'),
    path('qa/', views.search_qa, name="qa"),
    path('', views.search_index, name="search"),
]
