from rest_framework import serializers
from .models import Tresorerie

class TresorerieSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()  # Affiche le nom de l'utilisateur au lieu de son ID

    class Meta:
        model = Tresorerie
        fields = '__all__'
