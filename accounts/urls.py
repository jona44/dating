from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("welcome/", views.welcome_view, name="welcome"),
    path("onboarding/<int:step>/", views.onboarding_step_view, name="onboarding_step"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("photo/<uuid:photo_id>/delete/", views.delete_photo_view, name="delete_photo"),
    
    # Password Reset URLs
    path("password-reset/", 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
         ), 
         name="password_reset"),
    path("password-reset/done/", 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name="password_reset_confirm"),
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name="password_reset_complete"),
]
