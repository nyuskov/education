from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Article
        fields = "__all__"
