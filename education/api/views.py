from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext as _
from blog.models import Article
from .serializers import ArticleSerializer


class HelloApiView(GenericAPIView):
    def get(self, request: Request) -> Response:
        return Response(
            {"message": "{}!".format(_("Hello World"))})


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "title",
        "message"
    ]
    filterset_fields = [
        "title",
        "message",
        "author",
    ]
    ordering_fields = [
        "title",
        "message",
        "author__username",
    ]
