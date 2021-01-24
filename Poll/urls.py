from django.contrib import admin
from django.urls import path, include

from Poll import views
from .utils import render_to_pdf

urlpatterns = [
    path('', views.login_view, name="login"),
    path('profile', views.profile_view, name="profile"),
    path('custom', views.view_welcome, name="welcome"),
    path('poll1/', views.view_form_profile_bs, name="poll-personal"),
    path('poll2/', views.view_form_profile_bm, name="poll-manager"),
    path('poll3/', views.view_form_sales, name="poll-sales"),
    path('poll4/', views.view_form_quantity, name="poll-quantity"),
    path('poll5/', views.view_form_process_list, name="poll-process-list"),
    path('poll6/', views.view_process, name="poll-process"),
    path('poll7/', views.view_control, name="poll-control"),
    path('poll8/', views.view_form_activity_list, name="poll-activity-list"),
    path('poll9/', views.view_activity, name="poll-activity"),
    path('poll-results/', views.view_results, name="poll-results"),
    path('logout', views.logout_view, name="logout"),
    path('pdf', views.GeneratePDF.as_view(), name="pdf"),

    path('update-manager', views.UpdateManagerView.as_view(), name="update-manager"),
    path('update-user', views.UpdateUserView.as_view(), name="update-user")
]
