from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission


class UserChangeViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser')

        self.client.force_login(self.user)

    def test_user_change_view_with_all_permissions(self):
        # Add permissions
        permission_viewprofile = Permission.objects.get(
            codename="view_profile"
        )
        permission_viewuser = Permission.objects.get(
            codename="view_user"
        )
        permission_changeuser = Permission.objects.get(
            codename="change_user"
        )
        permission_changeprofile = Permission.objects.get(
            codename="change_profile"
        )

        self.user.user_permissions.add(permission_viewprofile)
        self.user.user_permissions.add(permission_viewuser)
        self.user.user_permissions.add(permission_changeuser)
        self.user.user_permissions.add(permission_changeprofile)

        response = self.client.get(reverse("account:index", kwargs={
            "pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"],
                         "text/html; charset=utf-8")
        self.assertContains(response, "Change")

    def test_user_change_view_with_view_permissions(self):
        # Add permissions
        permission_viewprofile = Permission.objects.get(
            codename="view_profile"
        )
        permission_viewuser = Permission.objects.get(
            codename="view_user"
        )

        self.user.user_permissions.add(permission_viewprofile)
        self.user.user_permissions.add(permission_viewuser)

        response = self.client.get(reverse("account:index", kwargs={
            "pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"],
                         "text/html; charset=utf-8")
        self.assertNotContains(response, "Change")

    def test_user_change_view_without_permissions(self):
        response = self.client.get(reverse("account:index", kwargs={
            "pk": self.user.pk}))
        self.assertEqual(response.status_code, 403)

    def tearDown(self) -> None:
        self.user.delete()
