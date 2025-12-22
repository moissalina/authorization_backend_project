from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, UpdateProfileView, DeleteAccountView,
    OrdersView, RolesRulesView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", UpdateProfileView.as_view()),
    path("delete_account/", DeleteAccountView.as_view()),
    path("orders/", OrdersView.as_view()),
    path("roles_rules/", RolesRulesView.as_view()),
]
