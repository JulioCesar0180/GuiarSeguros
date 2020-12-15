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
    # path('poll6/', views.view_transport_process, name="poll-transport"),
    # path('poll7/', views.view_manufacture_process, name="poll-manufacture"),
    # path('poll8/', views.view_building_process, name="poll-building"),
    # path('poll9/', views.view_services_process, name="poll-services"),
    # path('poll10/', views.view_control_risk, name="poll-control-risk"),
    # path('poll11/', views.view_prevent_risk, name="poll-prevent-risk"),
    # path('poll6/', views.view_control_risk, name="poll-control-risk"),
    # path('poll7/', views.view_prevent_risk, name="poll-prevent-risk"),
    path('poll8/', views.view_form_activity_list, name="poll-activity-list"),
    # path('poll12/', views.view_confirmed_control_explosive, name="poll-confirmed-explosive"),
    # path('poll13/', views.view_control_explosive, name="poll-explosive"),
    # path('poll14/', views.view_confirmed_control_electricity, name="poll-confirmed-electricity"),
    # path('poll15/', views.view_control_electricity, name="poll-electricity"),
    # path('poll16/', views.view_confirmed_substances, name="poll-confirmed-substance"),
    # path('poll17/', views.view_control_substances, name="poll-substance"),
    # path('poll18/', views.view_confirmed_height, name="poll-confirmed-height"),
    # path('poll19/', views.view_control_height, name="poll-height"),
    path('poll-results/', views.view_results, name="poll-results"),
    path('logout', views.logout_view, name="logout"),
    path('pdf', views.GeneratePDF.as_view(), name="pdf"),

    path('poll-A/', views.view_process, name="poll-process"),
    path('poll-B/', views.view_control, name="poll-control"),
    path('poll-C/', views.view_activity, name="poll-activity"),

    path('update-manager', views.UpdateManagerView.as_view(), name="update-manager"),
    path('update-user', views.UpdateUserView.as_view(), name="update-user")
]
