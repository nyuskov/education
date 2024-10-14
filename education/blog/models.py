from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save


@receiver(pre_save, sender="blog.Comment")
def prevent_reverse_link(sender, instance, **kwargs):
    if instance.parent and instance.pk == instance.parent.pk:
        instance.parent = None
        raise ValidationError({"parent": "Can't add yourself"})


@receiver(pre_save, sender="blog.Comment")
def prevent_crossed_link(sender, instance, **kwargs):
    if (instance.parent and
        instance.parent.parent and
            instance.pk == instance.parent.parent.pk):
        instance.parent = None
        raise ValidationError({"parent": "Can't add crossed links"})


@receiver(pre_save, sender="blog.Comment")
def prevent_crossed_article_link(sender, instance, **kwargs):
    if instance.parent and instance.parent.article.pk != instance.article.pk:
        instance.parent = None
        raise ValidationError({"parent": "Can't add crossed article links"})


class Article(models.Model):
    class Meta:
        ordering = ['title']

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    message = models.TextField()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    class Meta:
        ordering = ('created_at',)

    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Attachment(models.Model):
    class Meta:
        ordering = ('created_at',)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    message = models.FileField(upload_to="blog/comments/")
    created_at = models.DateTimeField(auto_now_add=True)
