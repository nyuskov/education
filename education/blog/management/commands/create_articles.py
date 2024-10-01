from random import randint
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Article


class Command(BaseCommand):
    """
    Creates articles
    """

    def handle(self, *args, **options):
        self.stdout.write("Create articles")
        letters = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й",
                   "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф",
                   "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

        user = User.objects.get(pk=randint(1, 2))
        for i in range(3):
            article, created = Article.objects.get_or_create(
                author=user,
                title=letters[randint(0, 32)] * randint(1, 10), message=letters[
                    randint(0, 32)] * randint(1, 100))
            self.stdout.write(f"Created article {article.title}")

        self.stdout.write(self.style.SUCCESS("Articles created"))
