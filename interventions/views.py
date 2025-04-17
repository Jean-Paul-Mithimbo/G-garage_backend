from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Client, Vehicule, Panne, EquipeReparation, Intervention, HistoriqueReparation
from .serializers import (
    ClientSerializer, VehiculeSerializer, PanneSerializer, EquipeReparationSerializer,
    InterventionSerializer, HistoriqueReparationSerializer
)

class ListeClients(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DetailClient(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ListeVehicules(generics.ListAPIView):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer

class ListePannes(generics.ListAPIView):
    queryset = Panne.objects.all()
    serializer_class = PanneSerializer

class ListeEquipes(generics.ListAPIView):
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
