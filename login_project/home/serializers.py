from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'endereco')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Senhas não conferem"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Usuario.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()