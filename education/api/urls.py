from django.urls import path
from .views import HelloApiView

app_name = "api"
urlpatterns = [
    path('hello/', HelloApiView.as_view(), name='hello'),

]
