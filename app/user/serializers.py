"""
    Serializers for the user API View
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'password2'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'username': {
                'help_text':
                "Username should be either an email or a phone number"
            }
        }

    def validate_username(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value) and \
                not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError(
                'Username should be either an email or a phone number.'
            )
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and confirm password do not match."
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        return user
