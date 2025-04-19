from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    contact = PhoneNumberField(region="CD")  # Validation automatique

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password', 'role', 'contact']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            role=validated_data['role'],
            contact=validated_data['contact']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
# 🔹 Sérialiseur pour récupérer les informations utilisateur
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','last_name', 'email', 'role', 'contact']
        # fields= '__all__'
