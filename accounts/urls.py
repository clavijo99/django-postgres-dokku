from django.urls import path, include
from rest_framework import routers
from .api import UserDetailAPIView, CurrentUserAPIView, CustomObtainTokenPairWithView, \
    RegisterAPIView, LogoutAPIView, ResetPasswordRequestAPIView, ResetPasswordConfirmAPIView, CustomTokenRefreshView, \
    AvatarViewSet
from accounts.views import activate_account, password_reset_confirm

avatar_router = routers.DefaultRouter()
avatar_router.register('', AvatarViewSet, basename='emergencies')

api_urls = ([
    path('logout/', LogoutAPIView.as_view(), name='user-auth-logout'),
    path("current/", CurrentUserAPIView.as_view(), name="get-current-user"),
    path("login/", CustomObtainTokenPairWithView.as_view(), name="user-login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="user-refresh-token"),
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path("recover-password/", ResetPasswordRequestAPIView.as_view(), name="recover-password"),
    path("user/<str:username>/", UserDetailAPIView.as_view(), name="get-user-detail"),
    path('', include(avatar_router.urls)),

], 'users')

urlpatterns = [
    path('activate_account_success/', activate_account, name='activate-account'),
    path('password-reset-confirm/', password_reset_confirm, name='password-reset-confirm'),
]
