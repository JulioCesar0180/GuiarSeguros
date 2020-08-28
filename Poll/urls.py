from django.contrib import admin
from django.urls import path, include

from Poll import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('profile', views.profile_view, name="profile"),
    path('custom', views.view_welcome, name="welcome"),
    path('poll', views.poll_view, name="poll"),

    path('poll1', views.FormProfileBSPoll.as_view(), name="poll-personal"),
    path('poll2', views.FormProfileMSPoll.as_view(), name="poll-manager"),
    path('poll3', views.FormSalesPoll.as_view(), name="poll-sales"),
    path('poll4', views.FormQuantityPoll.as_view(), name="poll-quantity"),
    path('poll5', views.FormProcessPoll.as_view(), name="poll-process"),

    path('poll-risk', views.poll_risk, name="poll-risk"),
    path('logout', views.logout_view, name="logout"),
]
