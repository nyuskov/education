from django.urls import reverse_lazy
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, FormView
from .forms import ArticleCreateForm, ArticleForm
from .models import Article


class ArticleCreateView(CreateView):
    form_class = ArticleCreateForm
    template_name = 'blog/create_article.html'
    success_url = reverse_lazy('/')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        data['author'] = request.user
        form = ArticleCreateForm(data)

        if form.is_valid():
            form.save()
            result = 'Article was created!'
        else:
            result = "Article wasn't created!"

        return render(request, template_name='blog/create_article.html',
                      context={
                          'form': form,
                          'result': result
                      })


class ArticleView(FormView):
    form_class = ArticleForm
    template_name = 'blog/index.html'

    def get(self, request, *args, **kwargs):
        search_word = request.GET.get('search', '')

        if search_word:
            articles = Article.objects.filter(
                title__icontains=search_word
            )
        else:
            articles = Article.objects.all()

        paginator = Paginator(articles, 5)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            "page_obj": page_obj,
            "search": search_word
        })
