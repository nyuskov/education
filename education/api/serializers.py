from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Article


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

    def save(self):
        if self.validated_data.get('author'):
            self.validated_data['author'] = User.objects.get(
                username=self.validated_data['author'])

        return super().save()
