"""
URL configuration for education project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (
    ArticleCreateView,
    ArticleUpdateView,
    ArticleView,
    ArticleDeleteView,
    ArticleExportView,
    CommentDeleteView
)

app_name = 'blog'
urlpatterns = [
    path('', ArticleView.as_view(), name='index'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete'),
    path('<int:pk>/delete-comment/', CommentDeleteView.as_view(),
         name='delete_comment'),
    path('export/', ArticleExportView.as_view(), name='export'),
]
