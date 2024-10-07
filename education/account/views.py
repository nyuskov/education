from django.contrib.auth.views import LoginView
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from .forms import (CustomUserCreationForm,
                    CustomAuthenticationForm,
                    CustomUserForm)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:signin')


class SignInView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'account/signin.html'
    redirect_authenticated_user = True


class UserChangeView(UpdateView):
    form_class = CustomUserForm
    template_name = 'account/profile.html'

    def get_queryset(self):
        return User.objects.prefetch_related(
            'groups', 'user_permissions')

    def get_success_url(self) -> str:
        return reverse("account:index", kwargs={"pk": self.object.pk})
