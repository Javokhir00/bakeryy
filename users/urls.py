from django.urls import path
from .views import CustomLoginView, CustomRegisterView, CustomLogoutView, simple_logout

app_name = 'users'

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout-simple/', simple_logout, name='logout_simple'),
]