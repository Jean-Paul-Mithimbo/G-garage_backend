from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Devis, Facture, Paiement, Abonnement, Fidélité
from .serializers import (
    ClientSerializer, DevisSerializer, FactureSerializer, 
    PaiementSerializer, AbonnementSerializer, FideliteSerializer
)

class ListeClients(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DetailClient(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ListeDevis(generics.ListAPIView):
    queryset = Devis.objects.all()
    serializer_class = DevisSerializer

class ListeFactures(generics.ListAPIView):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer

class ListePaiements(generics.ListAPIView):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

class ListeAbonnements(generics.ListAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer

class ListeFidelites(generics.ListAPIView):
    queryset = Fidélité.objects.all()
    serializer_class = FideliteSerializer

class VerifierStatutFacture(APIView):
    def get(self, request, pk, format=None):
        facture = generics.get_object_or_404(Facture, pk=pk)
        return Response({'facture_id': facture.id, 'statut': facture.statut})
