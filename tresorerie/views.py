from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Tresorerie
from .serializers import TresorerieSerializer

class ListeTresorerie(generics.ListAPIView):
    queryset = Tresorerie.objects.all()
    serializer_class = TresorerieSerializer

class DetailTresorerie(generics.RetrieveAPIView):
    queryset = Tresorerie.objects.all()
    serializer_class = TresorerieSerializer

class AjouterTransaction(generics.CreateAPIView):
    queryset = Tresorerie.objects.all()
    serializer_class = TresorerieSerializer

class RapportFinancier(APIView):
    def get(self, request, format=None):
        total_entrees = Tresorerie.objects.filter(type_transaction='entree').aggregate(Sum('montant'))['montant__sum'] or 0
        total_sorties = Tresorerie.objects.filter(type_transaction='sortie').aggregate(Sum('montant'))['montant__sum'] or 0
        solde = total_entrees - total_sorties
        
        return Response({
            'total_entrees': total_entrees,
            'total_sorties': total_sorties,
            'solde': solde,
        })
