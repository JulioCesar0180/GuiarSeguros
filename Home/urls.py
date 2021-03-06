from django.urls import path

from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.view_register_manager, name='signUp'),

    #New Reset Password
    path('recuperar/', views.recuperar_password, name="recuperar"),
    path('token_recovery/', views.token_recovery, name="codigo"),

    # Reset Password Views
    #path('recovery/', views.PasswordResetViewGS.as_view(), name="recovery"),
    #path('recovery/done', views.PasswordResetDoneViewGS.as_view(), name="recovery_done"),
    #path('recovery-pass/<uidb64>/<token>', views.PasswordResetConfirmViewGS.as_view(), name="recovery-pass-confirm"),
    #path('recovery-success', views.PasswordResetCompleteViewGS.as_view(), name="recovery-complete"),

    path('change_password', views.change_password_view, name="change_password"),
]
