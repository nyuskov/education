from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


ArticleFormSet = forms.modelformset_factory(
    Article, form=ArticleForm, formset=forms.BaseModelFormSet, extra=0)
