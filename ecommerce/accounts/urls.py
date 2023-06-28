from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register, name="register"),
    # // eamil verification
    path(
        "email-verification/<str:uidb64>/<str:token>/",
        views.email_verification,
        name="email-verification",
    ),
    path(
        "email-verification-sent/",
        views.email_verification_sent,
        name="email-verification-sent",
    ),
    path(
        "email-verification-failed/",
        views.email_verification_failed,
        name="email-verification-failed",
    ),
    path(
        "email-verification-success/",
        views.email_verification_success,
        name="email-verification-success",
    ),
    path("user-login/", views.user_login, name="user-login"),
    path("user-logout/", views.user_logout, name="user-logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    # path('profile-update/', views.profile_update, name='profile-update'),
    path("delete-account/", views.delete_account, name="delete-account"),
    # password reset
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password/password-reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("manage-shipping/", views.manage_shipping, name="manage-shipping"),
    path("manage-orders/", views.manage_orders, name="manage-orders"),
]
