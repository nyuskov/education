from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Article
from .admin_mixins import ExportAsCSVMixin

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = ["export_csv"]
    list_display = "pk", "title", "message_short", "author_verbose"
    list_display_links = "pk", "title"
    ordering = "title", "pk"
    search_fields = "title", "message"
    fieldsets = [
        (None, {
            "fields": ("title", "message")
        }),
        ("Author option", {
            "fields": ("author",),
            "classes": ("collapse",)
        }),
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Article.objects.select_related("author")

    def message_short(self, obj: Article) -> str:
        if len(obj.message) < 48:
            return obj.message
        return obj.message[:48] + '...'

    def author_verbose(self, obj: Article) -> str:
        return obj.author.first_name or obj.author.username
