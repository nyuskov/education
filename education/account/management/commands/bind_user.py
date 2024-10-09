from typing import Any
from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        user = User.objects.get(pk=3)
        group, created = Group.objects.get_or_create(
            name="profile_manager"
        )
        permission_profile = Permission.objects.get(
            codename="view_profile"
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry"
        )
        permission_changeprofile = Permission.objects.get(
            codename="change_profile"
        )
        permission_viewprofile = Permission.objects.get(
            codename="view_profile"
        )
        permission_viewuser = Permission.objects.get(
            codename="view_user"
        )
        permission_changeuser = Permission.objects.get(
            codename="change_user"
        )

        # Добавление разрешения в группу
        group.permissions.add(permission_profile)

        # Добавление пользователя в группу
        user.groups.add(group)

        # Связывание пользователя с разрешением
        user.user_permissions.add(permission_logentry)
        user.user_permissions.add(permission_changeprofile)
        user.user_permissions.add(permission_viewprofile)
        user.user_permissions.add(permission_viewuser)
        user.user_permissions.add(permission_changeuser)

        group.save()
        user.save()
