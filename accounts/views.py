from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import FormView, UpdateView, DetailView
from . import models, forms, mixins


class UserLoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "accounts/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("post:home")
    context_object_name = "forms"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            messages.success(self.request, f"어서오세요. {username}님")
            login(self.request, user)
        return super().form_valid(form)


@login_required
def log_out(request):
    messages.info(request, "로그아웃하였습니다.")
    logout(request)
    return redirect(reverse("post:home"))


class SignupView(mixins.LoggedOutOnlyView, FormView):
    template_name = "accounts/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("post:home")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            messages.success(self.request, f"어서오세요. {username}님")
            login(self.request, user)
        return super().form_valid(form)


class ProfileView(DetailView):
    model = models.User
    template_name = "accounts/profile.html"
    context_object_name = "user_obj"


class UpdateProfileView(UpdateView):
    model = models.User
    template_name = "accounts/update_profile.html"
    context_object_name = "user_obj"
    fields = (
        "nickname",
        "avatar",
        "bio",
    )

    def get_object(self, queryset=None):
        return self.request.user


class ChangePassword(PasswordChangeView):
    template_name = "accounts/change_password.html"
