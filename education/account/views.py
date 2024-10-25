import logging

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from .forms import (CustomUserCreationForm,
                    CustomAuthenticationForm,
                    CustomUserForm,
                    CustomProfileForm)
from .models import Profile

logger = logging.getLogger(__name__)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:signin')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        return response


class SignInView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'account/signin.html'
    redirect_authenticated_user = True


class UserChangeView(PermissionRequiredMixin, UpdateView):
    permission_required = ("account.view_profile", "auth.view_user",)
    template_name = 'account/profile.html'
    form_class = CustomUserForm

    def get_context_data(self, profile_form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_form"] = profile_form or CustomProfileForm(
            instance=getattr(self.object, "profile", None))
        logger.info("User account data: %s", context)

        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.method == "POST":
            if getattr(self.object, "profile", None):
                data = self.request.POST.dict()
                data["user"] = self.object
                profile_form = CustomProfileForm(
                    data,
                    instance=self.object.profile
                )
                if profile_form.is_valid():
                    profile_form.save()
                else:
                    return self.render_to_response(
                        self.get_context_data(
                            profile_form=profile_form,
                            form=form))
            else:
                Profile.objects.create(
                    user=self.object,
                    bio=self.request.POST.get("bio"),)

        return response

    def get_queryset(self):
        return User.objects.prefetch_related(
            'groups', 'user_permissions')

    def get_success_url(self) -> str:
        return reverse("account:index", kwargs={"pk": self.object.pk})
