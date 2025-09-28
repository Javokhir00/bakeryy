from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('shop:index')
    
    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return reverse_lazy('shop:index')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('shop:index')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please log in with your credentials.")
        return response


def simple_logout(request):
    """Simple logout function as backup"""
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('shop:index')


