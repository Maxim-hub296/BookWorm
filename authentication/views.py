from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from cart.models import Cart


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("shop:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, "Thank you for registering")


        user = authenticate(username=username, password=form.cleaned_data.get('password1'))

        if user is not None:
            login(self.request, user)
            Cart.objects.get_or_create(user=user)
        return response

    def form_invalid(self, form):
        messages.error(self.request, f"{form.errors}")

class MyLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


    def get_success_url(self):
        messages.success(self.request, "You have successfully logged in")
        return reverse_lazy("shop:home")

    def form_invalid(self, form):
        messages.error(self.request, "Неверное имя или пароль")
        return super().form_invalid(form)

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("shop:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have successfully logged out")
        return super().dispatch(request, *args, **kwargs)