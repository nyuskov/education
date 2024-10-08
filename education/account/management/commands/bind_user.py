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

        # Добавление разрешения в группу
        group.permissions.add(permission_profile)

        # Добавление пользователя в группу
        user.groups.add(group)

        # Связывание пользователя с разрешением
        user.user_permissions.add(permission_logentry)

        group.save()
        user.save()
