from django.contrib import admin
from django.urls import path, include

from Poll import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('profile', views.profile_view, name="profile"),
    path('custom', views.view_welcome, name="welcome"),
    path('poll', views.poll_view, name="poll"),
    path('poll1', views.FormProfileBSPoll.as_view(), name="poll-personal"),
    path('poll2/<rut_bm>', views.FormProfileMSPoll.as_view(), name="poll-manager"),
    path('logout', views.logout_view, name="logout"),
]
