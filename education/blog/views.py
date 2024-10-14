from typing import Any
from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import ArticleForm
from .models import Article, Comment


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    permission_required = "blog.add_article"
    template_name = 'blog/create_article.html'
    success_url = reverse_lazy('blog:create')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['author'] = self.request.user

        return kwargs

    def form_valid(self, form):
        if self.request.method == "POST":
            messages.success(self.request, "{}!".format(
                _("Article was created")))

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.method == "POST":
            messages.error(self.request, "{}!".format(
                _("Article wasn't created")))

        return super().form_invalid(form)


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = "blog.delete_article"
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('blog:index')


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = "blog.delete_comment"
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('blog:index')


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    permission_required = "blog.change_article"
    template_name = 'blog/update_article.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['author'] = self.request.user

        return kwargs

    def get_success_url(self) -> str:
        return reverse(
            "blog:update",
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        if self.request.method == "POST":
            messages.success(self.request, "{}!".format(
                _("Article was updated")))

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.method == "POST":
            messages.error(self.request, "{}!".format(
                _("Article wasn't updated")))

        return super().form_invalid(form)


class ArticleView(PermissionRequiredMixin, ListView):
    queryset = Article.objects.select_related(
        'author').prefetch_related(
        'comment_set', 'comment_set__attachment_set')
    paginate_by = 5
    permission_required = "blog.view_article"
    template_name = 'blog/index.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        if self.request.method == 'GET':
            search_word = self.request.GET.get('search', '')

            if search_word:
                queryset = queryset.filter(
                    title__icontains=search_word
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            context["search"] = self.request.GET.get('search', '')

        return context


class ArticleExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        articles = Article.objects.order_by("pk").all()
        articles_data = [
            {
                "pk": article.pk,
                "title": article.title,
                "message": article.message,
            }
            for article in articles
        ]
        return JsonResponse({"articles": articles_data})
