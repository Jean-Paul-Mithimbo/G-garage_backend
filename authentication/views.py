from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from .serializers import RegisterSerializer, UserSerializer
from django.db.utils import IntegrityError
from rest_framework import status  # Import the status module

User = get_user_model()

# 🔹 Inscription d'un nouvel utilisateur

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Check for duplicate contact or email
            contact = serializer.validated_data.get('contact')
            email = serializer.validated_data.get('email')
            if User.objects.filter(contact=contact).exists():
                return Response({"error": "Cette personne existe déjà avec ce numéro de téléphone."}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({"error": "Cette personne existe déjà avec cette adresse e-mail."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user only if no errors
            self.perform_create(serializer)
            return Response({
                "message": "Inscription réussie.",
                "user": UserSerializer(serializer.instance).data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Handle validation errors from the serializer
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            # Handle database integrity errors
            error_message = "Conflit de données, veuillez vérifier les informations saisies."
            if 'contact' in str(e).lower():
                error_message = "Le numéro de téléphone est déjà utilisé."
            elif 'email' in str(e).lower():
                error_message = "L'adresse e-mail est déjà utilisée."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle unexpected errors
            return Response({"error": "Erreur inattendue. Veuillez réessayer plus tard."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
