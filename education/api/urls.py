from django.urls import path, include
from .views import HelloApiView, ArticleViewSet
from rest_framework.routers import DefaultRouter

app_name = "api"

routers = DefaultRouter()
routers.register("articles", ArticleViewSet)

urlpatterns = [
    path("hello/", HelloApiView.as_view(), name="hello"),
    path("", include(routers.urls)),
]
