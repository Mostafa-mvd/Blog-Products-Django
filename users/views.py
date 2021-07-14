from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from datetime import datetime
from users.forms import LoginForm
import logging


logger = logging.getLogger(__name__)

# Create your views here.


def login_view(request):
    login_form = LoginForm()
    context = {"login_form": login_form}
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user_obj = authenticate(request, username=username, password=password)

            if user_obj is not None:
                login(request, user_obj)
                next_url = request.GET.get("next", reverse("blog:post_list"))
                if is_safe_url(next_url, settings.ALLOWED_HOSTS):
                    logger.info(f"User Logged in at {datetime.now()}")
                    return redirect(next_url)
                else:
                    return redirect("blog:post_list")
            else:
                messages.error(request, "Your username and password are incorrect. ")
    return render(request, "users/login.html", context)


def logout_user(request):
    logout(request)
    logger.info(f"User Logged out at {datetime.now()}")

    return redirect("users:login_user")


class EditUserProfile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = (
        "first_name",
        "last_name",
        "email"
    )
    template_name = "users/user_form.html"
    success_url = reverse_lazy("blog:post_list")

    # It returns an object (an instance of your model)
    def get_object(self, queryset=None):
        return self.request.user
