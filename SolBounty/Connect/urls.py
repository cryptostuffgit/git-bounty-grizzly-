from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, exchange_token, link_repository, get_issues, create_issue_api, github_webhook, check_user, get_bounties, apply_issue_api
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='register'),
    path('accounts/logout', LogoutView.as_view(), name='register'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('social/<str:backend>', exchange_token, name='github'),
    path('link-repository', link_repository, name='link-repository'),
    path('get-open-issues', get_issues, name='get-open-issues'),
    path('create-issue', create_issue_api, name='create-issue'),
    path('github/webhook', github_webhook, name='github-webhook'),
    path('check-user',check_user,name='check_user'),
    path('get-bounties',get_bounties,name='get-bounties'),
    path('apply-issue',apply_issue_api,name='apply-issue')
]