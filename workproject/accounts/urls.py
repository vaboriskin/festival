# accounts/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('password/', views.password_page, name='password_page'),
    path('signup/', views.signup_view, name='signup'),  # URL для регистрации
    path('login/', views.login_view, name='login'),      # URL для входа
]
