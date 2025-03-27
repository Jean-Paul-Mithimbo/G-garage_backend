from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

# 🔹 Inscription d'un nouvel utilisateur
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# 🔹 Récupération du profil utilisateur
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 🔹 Déconnexion (révoque le token)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Déconnexion réussie"}, status=200)
    except Exception as e:
        return Response({"error": "Échec de la déconnexion"}, status=400)
