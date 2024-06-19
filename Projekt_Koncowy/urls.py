"""
URL configuration for Projekt_Koncowy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import django.contrib.auth.views as auth_views

from evently.views import create_event, UserCreationView, CreateCategoryView, list_events, subscribe_event, \
    search_event

urlpatterns = [
    path('admin/', admin.site.urls),

    path('event/', create_event, name='event'),  # Tworzenie eventu

    path("CreateCategory", CreateCategoryView.as_view(), name="create_category"),  # Tworzenie kategori

    path('list_events/', list_events, name='list_events'),  # Lista eventow

    path('search', search_event, name='search_event'),

    path('subscribe/<int:event_id>/', subscribe_event, name='subscribe_event'),  # dodano event_id

    # Zarzadzanie uzytkownikiem
    path('createuser/', UserCreationView.as_view(), name='user'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # new

]
