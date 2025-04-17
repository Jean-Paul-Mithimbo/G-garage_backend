from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Devis, Abonnement, Fidélité
from .serializers import (
    ClientSerializer, DevisSerializer, AbonnementSerializer, FideliteSerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DevisViewSet(viewsets.ModelViewSet):
    queryset = Devis.objects.all()
    serializer_class = DevisSerializer


class AbonnementsViewSet(viewsets.ModelViewSet):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer

class FidelitesViewSets(viewsets.ModelViewSet):
    queryset = Fidélité.objects.all()
    serializer_class = FideliteSerializer

