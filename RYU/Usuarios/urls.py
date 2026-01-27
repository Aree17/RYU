from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="auth/password_reset.html"
    ), name="password_reset"),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="auth/password_reset_done.html"
    ), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="auth/password_reset_confirm.html"
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="auth/password_reset_complete.html"
    ), name="password_reset_complete"),

    path("perfil/", views.perfil_view, name="perfil"),
    path("perfil/cambiar-password/", views.cambiar_password_view, name="cambiar_password"),
    path("landing/", views.landing_view, name="landing"),
]
