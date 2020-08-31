from django.contrib import admin
from django.urls import path, include

from Poll import views
from .views import GeneratePDF

urlpatterns = [
    path('', views.login_view, name="login"),
    path('profile', views.profile_view, name="profile"),
    path('custom', views.view_welcome, name="welcome"),
    path('poll1/<int:pk>', views.view_form_profile_bs, name="poll-personal"),
    path('poll2/<int:pk>', views.view_form_profile_bm, name="poll-manager"),
    path('poll3/<int:pk>', views.view_form_sales, name="poll-sales"),
    path('poll4/<int:pk>', views.view_form_quantity, name="poll-quantity"),
    path('poll5/<int:pk>', views.view_form_process, name="poll-process"),
    path('poll6/<int:pk>', views.view_transport_process, name="poll-transport"),
    path('poll7/<int:pk>', views.view_manufacture_process, name="poll-manufacture"),
    path('poll8/<int:pk>', views.view_building_process, name="poll-building"),
    path('poll9/<int:pk>', views.view_services_process, name="poll-services"),
    path('poll10/<int:pk>', views.view_control_risk, name="poll-control-risk"),
    path('poll11/<int:pk>', views.view_prevent_risk, name="poll-prevent-risk"),
    path('poll12/<int:pk>', views.view_confirmed_control_explosive, name="poll-confirmed-explosive"),
    path('poll13/<int:pk>', views.view_control_explosive, name="poll-explosive"),
    path('poll14/<int:pk>', views.view_confirmed_control_electricity, name="poll-confirmed-electricity"),
    path('poll15/<int:pk>', views.view_control_electricity, name="poll-electricity"),
    path('poll16/<int:pk>', views.view_confirmed_substances, name="poll-confirmed-substance"),
    path('poll17/<int:pk>', views.view_control_substances, name="poll-substance"),
    path('poll18/<int:pk>', views.view_confirmed_height, name="poll-confirmed-height"),
    path('poll19/<int:pk>', views.view_control_height, name="poll-height"),
    path('poll-results/<int:pk>', views.view_results, name="poll-results"),
    path('logout', views.logout_view, name="logout"),
    path('pdf', views.GeneratePDF, name="pdf"),
]
