from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from weblinks.views import search_weblinks
from . import views
from django.urls import path
from accounts.views import google_login, google_callback, logout, login_view
from .views import profile, share_weblink, user_list

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(
        "logout/", logout, name="logout"
    ),
    path("profile/", views.profile, name="profile"),
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path("search/", search_weblinks, name="search_weblinks"),
    path("users/", user_list, name="user_list"),
    path("share/<int:weblink_id>/", share_weblink, name="share_weblink"),
    path("search/", search_weblinks, name="search_weblinks"),
]
