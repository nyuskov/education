
import math

from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Article


class ArticleCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser')

        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.user.delete()
        Article.objects.all().delete()

    def test_create_article(self):
        # Create article
        permission_addarticle = Permission.objects.get(
            codename="add_article"
        )
        self.user.user_permissions.add(permission_addarticle)

        response = self.client.post(
            reverse("blog:create"),
            {
                "author": self.user.id,
                "title": "Ghost is a soul",
                "message": "Message for this title",
            }
        )
        self.assertRedirects(response, reverse('blog:create'))

        # Get after it was created
        self.assertTrue(Article.objects.filter(
            title="Ghost is a soul").exists())

        permission_viewarticle = Permission.objects.get(
            codename="view_article"
        )
        self.user.user_permissions.add(permission_viewarticle)

        response = self.client.get(reverse("blog:index"))
        self.assertContains(response, "Ghost is a soul")


class ArticleViewTestCase(TestCase):
    fixtures = [
        'auth_fixtures.json',
        'articles_fixtures.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(username='testuser')

        permission_viewarticle = Permission.objects.get(
            codename="view_article"
        )
        cls.user.user_permissions.add(permission_viewarticle)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_articles_without_permissions(self):
        self.user.user_permissions.all().delete()
        response = self.client.get(reverse("blog:index"))

        self.assertEqual(response.status_code, 403)

    def test_articles_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("blog:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)

    def test_articles(self):
        # Get number of pages
        n_pages = math.ceil(Article.objects.count() / 5)

        # Number articles on page
        shift = 5

        # It is checking for all articles in page,
        # it is working, if articles' order in page equals articles' order in model
        for i in range(n_pages):
            offset = i*shift

            # Get a page
            response = self.client.get(
                reverse("blog:index"), QUERY_STRING=f"page={i+1}")

            # Get and check articles in page
            self.assertQuerySetEqual(
                qs=Article.objects.all()[offset:offset+shift],
                values=(article.title for article in response.context[
                    "page_obj"]),
                transform=lambda article: article.title,
            )
            self.assertTemplateUsed(response, "blog/index.html")


class ArticleExportViewTestCase(TestCase):
    fixtures = [
        'auth_fixtures.json',
        'articles_fixtures.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(username='testuser')

        permission_viewarticle = Permission.objects.get(
            codename="view_article"
        )
        cls.user.user_permissions.add(permission_viewarticle)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_article_view(self):
        response = self.client.get(reverse("blog:export"))
        self.assertEqual(response.status_code, 200)
        articles = Article.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": article.pk,
                "title": article.title,
                "message": article.message,
            }
            for article in articles
        ]
        articles_data = response.json()
        self.assertEqual(
            expected_data, articles_data["articles"],
        )
