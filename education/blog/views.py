from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from .forms import ArticleForm
from .models import Article


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/create_article.html'
    success_url = reverse_lazy('blog:create')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['author'] = self.request.user

        return kwargs

    def form_valid(self, form):
        if self.request.method == "POST":
            messages.success(self.request, "Article was created!")

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.method == "POST":
            messages.error(self.request, "Article wasn't created!")

        return super().form_invalid(form)


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('blog:index')


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
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
            messages.success(self.request, "Article was updated!")

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.method == "POST":
            messages.error(self.request, "Article wasn't updated!")

        return super().form_invalid(form)


class ArticleView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            search_word = self.request.GET.get('search', '')

            if search_word:
                articles = Article.objects.filter(
                    title__icontains=search_word
                ).select_related('author')
            else:
                articles = Article.objects.select_related('author')

            paginator = Paginator(articles, 5)
            page_number = int(self.request.GET.get("page", 1))
            if (page_number < 1):
                page_number = 1

            page_obj = paginator.get_page(page_number)

            context["page_obj"] = page_obj
            context["search"] = search_word

        return context
