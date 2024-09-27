from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    AUTHOR_CHOICES = [
        (author, author) for author in User.objects.values_list(
            'username', flat=True)
    ]
    author = serializers.ChoiceField(
        choices=AUTHOR_CHOICES)

    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
