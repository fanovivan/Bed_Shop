from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm


@login_not_required
def register(request):
    if request.user.is_authenticated:
        return redirect("shop:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Добро пожаловать, {user.username}! Регистрация прошла успешно.",
            )
            return redirect("shop:home")
    else:
        form = RegisterForm()

    return render(request, "shop/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "shop/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("shop:home")

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Вы вошли как {form.get_user().username}.",
        )
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("shop:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Вы вышли из аккаунта.")
        return super().dispatch(request, *args, **kwargs)
