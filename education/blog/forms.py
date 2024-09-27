from django import forms
from django.contrib.auth.models import User
from .models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleForm(forms.ModelForm):
    AUTHOR_CHOICES = [
        (author, author) for author in User.objects.values_list(
            'username', flat=True)
    ]
    author = forms.ChoiceField(choices=AUTHOR_CHOICES, widget=forms.Select(attrs={
        'class': 'blog-form__select',
    }))

    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


ArticleFormSet = forms.modelformset_factory(
    Article, form=ArticleForm, formset=forms.BaseModelFormSet, extra=0)
