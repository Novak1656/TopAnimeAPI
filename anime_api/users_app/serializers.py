from django.core.validators import MinLengthValidator
from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(validators=[MinLengthValidator(8)])

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def save(self, **kwargs):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({password: "Passwords don't match"})

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
