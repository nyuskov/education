from string import ascii_letters
from random import randint, choices
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Article


class Command(BaseCommand):
    """
    Creates articles
    """

    def handle(self, *args, **options):
        self.stdout.write("Create articles")

        user = User.objects.get(pk=randint(1, 2))
        for i in range(3):
            article = Article.objects.get_or_create(
                author=user,
                title="".join(choices(ascii_letters, k=randint(1, 10))),
                message="".join(choices(ascii_letters, k=randint(20, 100))))[0]
            self.stdout.write(f"Created article {article.title}")

        self.stdout.write(self.style.SUCCESS("Articles created"))
