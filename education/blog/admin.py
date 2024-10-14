from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms import ModelChoiceField
from django.http import HttpRequest
from .models import Article, Comment, Attachment
from .admin_mixins import ExportAsCSVMixin


class CommentInline(admin.StackedInline):
    model = Comment


class AttachmentInline(admin.StackedInline):
    model = Attachment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = ["export_csv"]
    list_display = "pk", "title", "message_short", "author_verbose"
    list_display_links = "pk", "title"
    ordering = "title", "pk"
    search_fields = "title", "message"
    inlines = [
        CommentInline,
    ]
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "edited_at",)
    list_display = ("pk", "message_short", "author_verbose",
                    "article_verbose", 'parent')
    list_display_links = "pk",
    inlines = [
        AttachmentInline
    ]
    ordering = "created_at", "edited_at", "pk"
    search_fields = "message", "author__username", "article__title"
    fieldsets = [
        (None, {
            "fields": ("message", "created_at", "edited_at")
        }),
        ("Author option", {
            "fields": ("author",),
            "classes": ("collapse",),
        }),
        ("Article option", {
            "fields": ("article",),
            "classes": ("collapse",),
        }),
        ("Parent comment option", {
            "fields": ("parent",),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Comment.objects.select_related(
            "article", "author", "parent")

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(
            request, obj=obj, change=change, **kwargs)

        if obj:
            form.base_fields['parent'] = ModelChoiceField(
                required=False, queryset=Comment.objects.exclude(
                    pk=obj.pk))

        return form

    def message_short(self, obj: Comment) -> str:
        if len(obj.message) < 48:
            return obj.message
        return obj.message[:48] + '...'

    def author_verbose(self, obj: Comment) -> str:
        return obj.author.first_name or obj.author.username

    def article_verbose(self, obj: Comment) -> str:
        return obj.article.title


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("pk", "message", "comment_id")
    list_display_links = "pk",
    ordering = "created_at", "pk"
    search_fields = "message",
    fieldsets = [
        (None, {
            "fields": ("message", "created_at")
        }),
        ("Comment option", {
            "fields": ("comment",),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Attachment.objects.select_related("comment")
