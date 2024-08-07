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
from django.urls import path
import django.contrib.auth.views as auth_views

from evently.views import create_event, UserCreateView, CreateCategoryView, list_events, subscribe_event, \
    search_event, edit_event, delete_event, full_event_description, unsubscribe_event,delete_comment,  linkedlin_Roger, \
    linkedlin_Artema, user_profile, user_subscriptions, homepage, admin_status_view, update_event_status, send_test_email

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    path("create_category", CreateCategoryView.as_view(), name="create_category"),  # uprawienia admina
    path("accept_status", admin_status_view, name="accept_status"),
    path('update_event_status/', update_event_status, name='update_event_status'),
    # główna strona
    path('', homepage, name='homepage'),
    # lista eventow
    path('list_events/', list_events, name='list_events'),
    # wyszukiwarka
    path('search/', search_event, name='search_event'),
    # zarządzanie eventem
    path('create_event/', create_event, name='create_event'),
    path('update_event/<int:pk>/', edit_event, name='event_edit'),
    path('delete_event/<int:pk>/', delete_event, name='delete_event'),
    path('full_event_description/<int:pk>/', full_event_description, name='full_event_description'),
    path('subscribe_event/<int:event_id>/', subscribe_event, name='subscribe_event'),
    path('event/<int:pk>/unregister/', unsubscribe_event, name='unsubscribe_event'),
    path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),
    # user
    path('createuser/', UserCreateView.as_view(), name='user'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # profile usera
    path('profile/', user_profile, name='user_profile'),
    path('profile/subscriptions/<pk>/', user_subscriptions, name='user_subscriptions'),  # forma "twoje subskrypcje"
    # zarządzanie hasłem
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # autorzy Evently
    path('Artem', linkedlin_Artema, name="Artem"),
    path('Roger', linkedlin_Roger, name="Roger"),
    path('send-email/', send_test_email, name='send_test_email'),
]
