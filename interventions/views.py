from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Vehicule, Panne, EquipeReparation, Intervention, Facture, HistoriqueReparation, LignePanne, MaterielUtilise
from clients.models import Client
from clients.serializers import ClientSerializer
from .serializers import (
    VehiculeSerializer, PanneSerializer,EquipeReparationSerializer,
    InterventionSerializer, FactureSerializer, HistoriqueReparationSerializer,
    LignePanneSerializer, MaterielUtiliseSerializer
)


# class ListeClients(generics.ListAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer

class DetailClient(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ListeVehicules(generics.ListAPIView):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer

class ListePannes(generics.ListAPIView):
    queryset = Panne.objects.all()
    serializer_class = PanneSerializer

class EquipesViewSet(viewsets.ModelViewSet):
    queryset = EquipeReparation.objects.all()
    serializer_class = EquipeReparationSerializer

class ListeInterventions(generics.ListAPIView):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer

class ListeHistoriques(generics.ListAPIView):
    queryset = HistoriqueReparation.objects.all()
    serializer_class = HistoriqueReparationSerializer

class AffecterEquipe(APIView):
    def post(self, request, intervention_id, equipe_id, format=None):
        try:
            intervention = Intervention.objects.get(id=intervention_id)
            equipe = EquipeReparation.objects.get(id=equipe_id)
            intervention.equipe = equipe
            intervention.save()
            return Response({'message': f'Équipe {equipe.nom} affectée à l\'intervention {intervention.id}.'})
        except (Intervention.DoesNotExist, EquipeReparation.DoesNotExist):
            return Response({'error': 'Intervention ou équipe introuvable.'}, status=404)

class CloturerIntervention(APIView):
    def post(self, request, intervention_id, format=None):
        try:
            intervention = Intervention.objects.get(id=intervention_id)
            if intervention.statut == 'en_cours':
                intervention.statut = 'terminee'
                intervention.date_fin_reelle = timezone.now()
                intervention.save()
                HistoriqueReparation.objects.create(intervention=intervention, details="Intervention terminée et archivée.")
                return Response({'message': f'Intervention {intervention.id} clôturée et archivée.'})
            return Response({'error': 'Intervention déjà clôturée ou annulée.'}, status=400)
        except Intervention.DoesNotExist:
            return Response({'error': 'Intervention introuvable.'}, status=404)

class VehiculeViewSet(viewsets.ModelViewSet):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer

class PanneViewSet(viewsets.ModelViewSet):
    queryset = Panne.objects.all()
    serializer_class = PanneSerializer

class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer

class LignePanneViewSet(viewsets.ModelViewSet):
    queryset = LignePanne.objects.all()
    serializer_class = LignePanneSerializer

class MaterielUtiliseViewSet(viewsets.ModelViewSet):
    queryset = MaterielUtilise.objects.all()
    serializer_class = MaterielUtiliseSerializer

class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer

class HistoriqueReparationViewSet(viewsets.ModelViewSet):
    queryset = HistoriqueReparation.objects.all()
    serializer_class = HistoriqueReparationSerializer
