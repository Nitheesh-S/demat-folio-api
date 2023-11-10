import re
import datetime
from cryptography import fernet

from rest_framework import serializers

from . import utils

def is_strong_password(password):
	if len(password) < 8:
		raise serializers.ValidationError('Password should be atleast 8 chars long')
    
	if not re.search(r'[A-Z]', password):
		raise serializers.ValidationError('Password should have atleast 1 uppercase')

	if not re.search(r'[a-z]', password):
		raise serializers.ValidationError('Password should have atleast 1 lowercase')

	if not re.search(r'[0-9]', password):
		raise serializers.ValidationError('Password should have atleast 1 digit')

	if not re.search(r'[!@#\$%^&*()_+{}\[\]:;<>,.?~]', password):
		raise serializers.ValidationError('Password should have atleast 1 special char')
	
	return password


def verify_email_token(token: str) -> int:
	try:
		message = utils.decrypt_message(token)
	except fernet.InvalidToken:
		raise serializers.ValidationError("Invalid token")
	
	created_time_str, user_pk_str = message.split("::")

	created_time = float(created_time_str)
	user_pk = int(user_pk_str)

	# Check if token is created within 1 day
	expiry_duration = datetime.timedelta(days=1)
	if datetime.datetime.fromtimestamp(created_time) < datetime.datetime.now() - expiry_duration:
		raise serializers.ValidationError("Token expired")

	return user_pk