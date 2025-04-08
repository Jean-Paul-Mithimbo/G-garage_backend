from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# 🔹 Sérialiseur pour l'inscription
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username','last_name', 'email', 'password', 'role', 'contact']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# 🔹 Sérialiseur pour récupérer les informations utilisateur
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'contact']
        # fields= '__all__'
