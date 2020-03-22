from rest_framework.routers import SimpleRouter

from elasticapp import views
from django.urls import path

urlpatterns = [
    path('', views.search_index, name = 'articles')
]


# app_name = 'elasticapp' 

# router = SimpleRouter()
# router.register(
#     prefix=r'',
#     basename='articles',
#     viewset=views.articles
# )
# urlpatterns = router.urls
