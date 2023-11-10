from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import serializers, status, permissions
from rest_framework.response import Response

from django.core.cache import cache
from django.conf import settings

from . import models, validators, services

from fyers_apiv3 import fyersModel


class SignUpApi(APIView):
	class InputSerializer(serializers.Serializer):
		name = serializers.CharField()
		email = serializers.EmailField()
		password_one = serializers.CharField(validators=[validators.is_strong_password])
		password_two = serializers.CharField(validators=[validators.is_strong_password])

		def validate(self, data):
			if data.get('password_one') != data.get('password_two'):
				raise serializers.ValidationError('Passwords doesn\'t match')
			
			return data

	def post(self, request):
		serializer = self.InputSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		print('serializer.validated_data -->', serializer.validated_data)

		if not serializer.validated_data:
			raise serializers.ValidationError('Invalid input')
		
		services.create_user(
			name=serializer.validated_data.get('name', None),
			email=serializer.validated_data.get('email', None),
			password=serializer.validated_data.get('password_one', None)
		)
		
		return Response({
			'data': 'success'
		})


class VerifyEmailApi(APIView):
	class InputSerializer(serializers.Serializer):
		token = serializers.CharField()

		def validate(self, data):
			user_pk = validators.verify_email_token(data.get('token'))
			data['user_id'] = user_pk
			return data
		
	def post(self, request):
		serializer = self.InputSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		print('serializer.validated_data -->', serializer.validated_data)

		user_id = serializer.validated_data.get('user_id', None)

		services.activate_user(user_id=user_id)

		return Response({
			'data': 'success'
		})


class SignInApi(APIView):
	class InputSerializer(serializers.Serializer):
		email = serializers.EmailField()
		password = serializers.CharField()

	def post(self, request):
		
		return Response({
			'data': 'success'
		})
	


class LoginFyersApi(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		user_id = request.GET.get('user_id', 'admin')

		appSession = fyersModel.SessionModel(
			client_id=settings.FYERS_CLIENT_ID, 
			redirect_uri=settings.FYERS_REDIRECT_URI,
			response_type="code",
			state=f"{user_id}",
			secret_key=settings.FYERS_SECRET_KEY,
			grant_type="authorization_code"
		)

		token_url = appSession.generate_authcode()

		return Response({
			"data": token_url
		})


class FyersCallback(APIView):
	def get(self, request):
		user_id = request.GET.get('user_id', 'admin')
		auth_code = request.GET.get('auth_code')
		
		appSession = fyersModel.SessionModel(
			client_id=settings.FYERS_CLIENT_ID, 
			redirect_uri=settings.FYERS_REDIRECT_URI,
			response_type="code",
			state=f"{user_id}",
			secret_key=settings.FYERS_SECRET_KEY,
			grant_type="authorization_code"
		)

		appSession.set_token(auth_code)
		response = appSession.generate_token()

		access_token = None
		try:
			access_token = response["access_token"]
			cache.set('FYERS_ACCESS_TOKEN', access_token, timeout=60 * 60 * 24)
		except Exception as e:
			print('Exception', e)
			print('response', response)

		return Response({
			"data": access_token
		})


class TestFyers(APIView):
	def get(self, request):
		fyers_access_token = cache.get('FYERS_ACCESS_TOKEN')
		print('fyers_access_token -->', fyers_access_token)
		if not fyers_access_token:
			return Response({
				"error": "Please Login with fyers to continue"
			}, status=status.HTTP_401_UNAUTHORIZED)
		
		fyers = fyersModel.FyersModel(
			token=fyers_access_token,
			is_async=False,
			client_id=settings.FYERS_CLIENT_ID
		)
		data = {"symbols":"NSE:GBEES-EQ"}
		quotes_data = fyers.quotes(data)
		return Response({
			"data": quotes_data
		})