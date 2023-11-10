from django.urls import path
from rest_framework.authtoken import views as drf_views

from portal import views


urlpatterns = [
	path("sign-up/", views.SignUpApi.as_view(), name="sign_up"),
	path("api-token-auth/", drf_views.obtain_auth_token, name="sign_in"),
	path("verify-email/", views.VerifyEmailApi.as_view(), name="verify_email_api"),
	path("login/fyers/", views.LoginFyersApi.as_view(), name="login_fyers"),
	path("fyers-callback/", views.FyersCallback.as_view(), name="fyers_callback"),
	path("test-fyers/", views.TestFyers.as_view(), name="test_fyers")
]