from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import (CustomUserCreationForm,
                    CustomAuthenticationForm,
                    CustomUserChangeForm)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:signin')


class SignInView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'account/signin.html'


class UserChangeView(FormView):
    form_class = CustomUserChangeForm
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        data = {
            'username': request.user.username,
            'password': request.user.password,
        }

        return render(request, template_name=self.template_name,
                      context={
                          'form': CustomUserChangeForm(
                              data)})
